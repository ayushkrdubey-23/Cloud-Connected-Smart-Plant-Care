# Project Workflow

```text
Virtual Sensor
      |
      v
Generate Sensor Data
      |
      v
FastAPI REST API
      |
      v
Validate Input
      |
      v
SQLite Storage
      |
      +------> Watering Engine
      |
      +------> Alert Service
      |
      v
React Dashboard
      |
      v
User
```

## User Actions
- Monitor plant conditions.
- Start manual watering.
- Refill the virtual tank.
- View watering history.
- View alerts.

## Automated Actions
- Receive sensor readings.
- Store readings.
- Evaluate moisture.
- Start/stop automatic watering.
- Consume virtual water.
- Generate alerts.
