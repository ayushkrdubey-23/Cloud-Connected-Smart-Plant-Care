# Database Design

The MVP uses SQLite with SQLAlchemy ORM.

## Device
Stores device and plant configuration.

| Field | Purpose |
|---|---|
| id | Primary key |
| device_id | Unique device identifier |
| plant_name | Plant name |
| plant_type | Plant profile |
| location | Device location |
| moisture_threshold | Target moisture |
| pump_status | Virtual pump state |
| auto_water | Automatic watering state |
| water_tank_level | Virtual tank percentage |
| last_seen | Last device activity |
| created_at | Creation time |

## SensorReading
Stores:
- device_id
- soil_moisture
- temperature
- humidity
- light_level
- timestamp

## WateringEvent
Stores:
- device_id
- trigger_type
- moisture_before
- moisture_after
- duration
- timestamp

## Alert
Stores:
- device_id
- alert_type
- message
- level
- status
- created_at

## Relationship

```text
Device
  +-- SensorReading
  +-- WateringEvent
  +-- Alert
```
