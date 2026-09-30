# Automatic Watering Logic

## Start Conditions

Automatic watering can start when:

```text
Automatic watering = ON
AND pump = OFF
AND soil moisture < configured threshold
AND water tank > minimum level
```

## Stop Conditions

Watering stops when:

```text
Soil moisture reaches threshold
OR maximum watering duration is reached
OR water tank reaches the minimum level
```

## Manual Watering
Manual watering is provided through:

```text
POST /api/watering/{device_id}/manual
```

The backend checks the device, pump state, and water-tank level.

## Water Consumption

```text
Water Consumed = Duration × Configured Consumption Rate
```

The calculated amount is deducted from the virtual tank.

## Plant Profiles

| Plant | Threshold |
|---|---:|
| Succulent | 20% |
| Tomato | 40% |
| Herb | 35% |
| Indoor Plant | 30% |
