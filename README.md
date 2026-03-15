# carepulse-health_monitor
AI-powered remote health monitoring system that analyzes patient's vitals and generates real-time health risk alerts and summaries.


## Problem Statement

Many patients, especially elderly individuals and people in remote areas, lack continuous access to healthcare monitoring. Early detection of abnormal vitals such as high heart rate, low oxygen levels, or fever can help prevent serious health complications.

This project aims to create an affordable remote health monitoring system that analyzes vital signs and provides automated alerts and AI-powered health insights.


## Solution

Our system allows users to input key health parameters including:

- Heart Rate
- Oxygen Saturation (SpO2)
- Body Temperature
- Symptoms

The backend analyzes these vitals using rule-based logic and generates alerts for abnormal conditions. Additionally, an AI model generates a short health summary to assist patients or doctors in understanding potential risks.

## Features

- Real-time health data input
- Automated health risk detection
- AI-generated health summaries
- API-based backend using Flask
- Data storage using SQLite
- Interactive API documentation using Swagger (Flasgger)


## Tech Stack

Frontend:
- HTML
- CSS

Backend:
- Python
- Flask

Database:
- SQLite

API Documentation:
- Flasgger (Swagger UI)

AI Integration:
- OpenAI API


## System Architecture

User Input (Vitals) --> Flask API Backend --> Health Logic Analysis --> SQLite Database Storage --> AI Health Summary Generation --> Alerts + Health Insights

## Installation and Setup

1. Clone the repository
2. Install required packages:

pip install flask flasgger openai

3. Add your OpenAI API key in app.py

4. Run the backend server:

python app.py

5. Open the API documentation:

http://127.0.0.1:5000/apidocs


## Example Output

Alerts:
- High Heart Rate
- Low Oxygen Level
- High Fever

AI Summary:
Patient shows signs of possible respiratory distress and high fever. Immediate medical consultation is recommended.


## Future Improvements

- Integration with wearable health devices
- Real-time monitoring using IoT sensors
- Doctor dashboard for patient monitoring
- Mobile application for remote healthcare access


## Contributors

Anushka Basak – Frontend Development (UI Design) + Backend Development (Python, Flask Integration, API, AI Integration)

Megha Chatterjee – Backend Development (Python, API, AI Integration)
