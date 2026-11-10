def analyze_health(heart_rate, spo2, temperature):
    alerts = []

    if heart_rate > 120:
        alerts.append("Very high heart rate detected")
    elif heart_rate > 100:
        alerts.append("Elevated heart rate detected")
    elif heart_rate < 50:
        alerts.append("Low heart rate detected")

    if spo2 < 90:
        alerts.append("Critically low oxygen level")
    elif spo2 < 94:
        alerts.append("Low oxygen level detected")

    if temperature > 39:
        alerts.append("High fever detected")
    elif temperature > 37.5:
        alerts.append("Mild fever detected")
    elif temperature < 35:
        alerts.append("Low body temperature detected")

    return alerts
