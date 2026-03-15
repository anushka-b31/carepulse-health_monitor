from flask import Flask, request, render_template
import sqlite3
from openai import OpenAI
from health_logic import analyze_health
from database import create_database

app = Flask(__name__)

# Create database
create_database()

# OpenAI client
client = OpenAI(api_key="openai_apikey")


@app.route("/")
def home():
    return render_template("index.html")


# AI Health Summary
def generate_health_summary(heart_rate, spo2, temperature, symptoms, risk_level):

    try:

        prompt = f"""
You are a healthcare assistant.

Patient vitals:
Heart Rate: {heart_rate} bpm
SpO2: {spo2}%
Temperature: {temperature}°C
Symptoms: {symptoms}

The system has already classified the patient as: {risk_level}.

Write a short 2-3 sentence explanation consistent with this classification.

Rules:
Low Risk → vitals appear normal
Moderate Risk → mild concern, recommend monitoring
High Risk → potential medical issue, recommend medical attention
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:

        print("OPENAI ERROR:", e)

        # fallback summaries
        if risk_level == "High Risk":
            return "Several abnormal vitals have been detected. Medical attention is recommended."

        elif risk_level == "Moderate Risk":
            return "Some vitals show mild abnormalities. Monitoring is recommended."

        else:
            return "The vitals appear within normal ranges."


@app.route("/submit", methods=["POST"])
def submit_data():

    heart_rate = int(request.form["heart_rate"])
    spo2 = int(request.form["spo2"])
    temperature = float(request.form["temperature"])
    symptoms = request.form["symptoms"]

    alerts = analyze_health(heart_rate, spo2, temperature)

    # -------------------------
    # RISK SCORING SYSTEM
    # -------------------------

    risk_score = 0

    # Heart rate
    if heart_rate > 120:
        risk_score += 4
    elif heart_rate > 100:
        risk_score += 2
    elif heart_rate > 90:
        risk_score += 1

    # Oxygen
    if spo2 < 90:
        risk_score += 5
    elif spo2 < 94:
        risk_score += 3
    elif spo2 < 97:
        risk_score += 1

    # Temperature
    if temperature > 39:
        risk_score += 4
    elif temperature > 38:
        risk_score += 3
    elif temperature > 37.5:
        risk_score += 1

    risk_percent = min(risk_score * 10, 100)
    risk_score=min(risk_score,10)
    # -------------------------
    # RISK LEVEL
    # -------------------------

    if risk_score <= 2:
        risk_level = "Low Risk"
        risk_color = "#27ae60"

    elif risk_score <= 5:
        risk_level = "Moderate Risk"
        risk_color = "#f39c12"

    else:
        risk_level = "High Risk"
        risk_color = "#e74c3c"

    # -------------------------
    # AI SUMMARY
    # -------------------------

    summary = generate_health_summary(
        heart_rate,
        spo2,
        temperature,
        symptoms,
        risk_level
    )

    # -------------------------
    # ALERT DISPLAY
    # -------------------------

    alerts_html = ""

    for alert in alerts:
        alerts_html += f"""
        <div style="
        background:#ffe6e6;
        padding:10px;
        margin:6px 0;
        border-radius:6px;
        color:#c0392b;
        font-weight:500;">
        ⚠ {alert}
        </div>
        """

    # -------------------------
    # SAVE TO DATABASE
    # -------------------------

    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO health_data (heart_rate, spo2, temperature, symptoms) VALUES (?, ?, ?, ?)",
        (heart_rate, spo2, temperature, symptoms)
    )

    conn.commit()
    conn.close()

    # -------------------------
    # RESULT PAGE
    # -------------------------

    return f"""
<html>

<body style="font-family:Segoe UI;background:linear-gradient(135deg,#4facfe,#00c6ff);margin:0;padding:40px;display:flex;justify-content:center;">

<div style="background:white;width:540px;padding:35px;border-radius:14px;box-shadow:0 12px 35px rgba(0,0,0,0.3);text-align:center;">

<h2 style="color:#2c3e50;">Health Analysis Report</h2>

<p><b>Heart Rate:</b> {heart_rate} bpm</p>
<p><b>SpO₂:</b> {spo2}%</p>
<p><b>Temperature:</b> {temperature} °C</p>
<p><b>Symptoms:</b> {symptoms}</p>

<hr>

<h3>Health Risk Level</h3>

<p style="font-weight:bold;color:{risk_color};font-size:18px;">
{risk_level}
</p>

<div style="background:#eee;border-radius:10px;height:22px;width:100%;margin-bottom:10px;">
<div style="background:{risk_color};width:{risk_percent}%;height:22px;border-radius:10px;"></div>
</div>

<p><b>Risk Score:</b> {risk_score}/10</p>

<hr>

<h3 style="color:#c0392b;">Health Alerts</h3>

{alerts_html}

<hr>

<h3 style="color:#2c3e50;">AI Health Summary</h3>

<p>{summary}</p>

<br>

<a href="/" style="
text-decoration:none;
background:#3498db;
color:white;
padding:10px 22px;
border-radius:6px;
font-weight:500;">
Back to Monitor
</a>

</div>

</body>

</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
