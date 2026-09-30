# System Architecture

## High-Level Architecture

```text
Virtual IoT Sensor Simulator
          |
       HTTP/REST
          v
     FastAPI Backend
       /    |    \
      v     v     v
   SQLite  Watering  Alerts
  Database  Engine   Service
       \     |     /
        \    |    /
         v   v   v
       React Dashboard
             |
            User
```

## Data Flow
1. Simulator generates sensor readings.
2. FastAPI receives and validates the payload.
3. Readings are stored in SQLite.
4. Automatic watering conditions are evaluated.
5. Alert conditions are evaluated.
6. The API returns the current state.
7. React displays live system information.

## Future Cloud Architecture

```text
ESP32 / IoT Sensors
        |
     Internet
        |
    Cloud API
        |
 Cloud Database
        |
 Automation / Alerts
        |
 Web or Mobile Dashboard
```
