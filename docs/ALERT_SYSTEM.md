# Alert System

## Current Alert Types

### LOW_MOISTURE
Generated when soil moisture is below the configured threshold.

### HIGH_TEMPERATURE
Generated when temperature exceeds the warning threshold.

### LOW_WATER_TANK
Generated when the virtual water tank reaches the critical level.

### DEVICE_OFFLINE
Generated when a device has not reported within the configured offline period.

## Alert Fields

```text
device_id
alert_type
message
level
status
created_at
```

Possible severity levels include:

```text
INFO
WARNING
CRITICAL
```

## Acknowledgement

Alerts can be acknowledged through the alert API.

## Future Improvement

A future version can automatically resolve an active alert when its condition returns to normal.
