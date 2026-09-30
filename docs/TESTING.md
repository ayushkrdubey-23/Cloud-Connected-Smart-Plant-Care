# Testing

## Automated Tests

Run:

```powershell
pytest
```

The watering-engine tests cover important cases including:
- Dry soil triggering watering.
- Moist soil preventing watering.
- Low tank preventing watering.
- Pump stopping.

## Manual Integration Test

1. Start FastAPI.
2. Open Swagger.
3. Check `/health`.
4. Send sensor data.
5. Verify latest reading.
6. Verify device status.
7. Test manual watering.
8. Run the simulator.
9. Verify watering history.
10. Verify tank consumption.
11. Refill the tank.
12. Check alerts.

## Frontend Verification

Verify:
- Live sensor values.
- Moisture chart.
- Plant health.
- Water tank.
- Manual watering.
- Refill.
- Watering history.
- Alerts.
