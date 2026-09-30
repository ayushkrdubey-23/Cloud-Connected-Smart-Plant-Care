# Project Report Summary

## Project Title
**Cloud-Connected Smart Plant Care & Watering System**

## Author
**Ayush Kumar Dubey**

## Abstract

The Cloud-Connected Smart Plant Care & Watering System is an IoT and Cloud Computing oriented prototype for monitoring plant conditions and automating watering. A virtual sensor simulator generates soil moisture, temperature, humidity, and light readings and sends them to a FastAPI backend. The backend validates and stores the readings in SQLite, evaluates automatic watering conditions, manages a virtual pump and virtual water tank, and generates alerts.

A React dashboard provides a visual interface for sensor monitoring, plant health, watering history, alerts, and tank status. Manual watering and tank refill are also supported.

The current version is a working educational MVP. Physical IoT hardware, cloud deployment, external notifications, production authentication, and advanced analytics are future extensions.

## Objectives
1. Monitor plant conditions.
2. Store sensor data.
3. Automate watering decisions.
4. Track virtual water consumption.
5. Generate alerts.
6. Provide a responsive dashboard.
7. Demonstrate a cloud-ready IoT architecture.

## Methodology

```text
Sensor Simulation
      ↓
REST API
      ↓
Validation
      ↓
Database
      ↓
Automation
      ↓
Alerts
      ↓
Dashboard
```

## Technologies
- Python
- FastAPI
- SQLAlchemy
- SQLite
- React
- Vite
- Recharts
- HTTPX
- Pydantic
- Pytest
- Git/GitHub

## Result

The MVP demonstrates end-to-end communication between a simulated IoT device, backend API, database, automation engine, alert system, and frontend dashboard.

## Limitations

The current version does not claim physical sensor integration, physical pump control, production cloud deployment, external notification services, or production-grade authentication.

## Future Scope

The system can be extended with ESP32 hardware, cloud databases, cloud hosting, mobile applications, notifications, machine-learning predictions, weather-aware watering, authentication, and multi-device support.

## Conclusion

The project demonstrates how IoT sensing, REST APIs, databases, automation, alerts, and frontend visualization can be combined into a smart plant-care system.

## Guidance

**Mr. Umesh Yadav**  
Founder, IIP

In collaboration with **eDC IIT Delhi**
