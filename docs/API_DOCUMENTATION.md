# API Documentation

## Base URL
```text
http://127.0.0.1:8000
```

## Swagger UI
```text
http://127.0.0.1:8000/docs
```

## Health
```text
GET /
GET /health
```

## Sensors
```text
POST /api/sensors/data
GET  /api/sensors/{device_id}/latest
GET  /api/sensors/{device_id}/history
GET  /api/sensors/{device_id}/status
```

Example sensor payload:

```json
{
  "device_id": "PLANT-001",
  "soil_moisture": 35.5,
  "temperature": 27.0,
  "humidity": 62.0,
  "light_level": 70.0
}
```

## Devices
```text
GET  /api/devices
POST /api/devices
GET  /api/devices/{device_id}
PUT  /api/devices/{device_id}
```

## Watering
```text
POST /api/watering/{device_id}/manual
POST /api/watering/{device_id}/refill
GET  /api/watering/{device_id}/history
```

## Alerts
```text
GET   /api/alerts/{device_id}
POST  /api/alerts/{device_id}/check-offline
PATCH /api/alerts/{alert_id}/acknowledge
```

Use Swagger for the exact request and response schemas of the running application.
