from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.orm import Session

from automation.watering_engine import WateringEngine
from backend.models import Device, WateringEvent


_engines: Dict[str, WateringEngine] = {}

VIRTUAL_WATER_TANK_LEVEL = 100.0
MINIMUM_WATER_TANK_LEVEL = 10.0

COOLDOWN_MINUTES = 0.5
MAXIMUM_DURATION_SECONDS = 20

# Virtual water consumption:
# 1 second of pump operation = 1% tank usage.
WATER_CONSUMPTION_PER_SECOND = 1.0


def get_engine(
    device_id: str,
    moisture_threshold: float,
) -> WateringEngine:
    """
    Get or create a watering engine for a virtual device.
    """

    if device_id not in _engines:
        _engines[device_id] = WateringEngine(
            moisture_threshold=moisture_threshold,
            minimum_water_tank=MINIMUM_WATER_TANK_LEVEL,
            cooldown_minutes=COOLDOWN_MINUTES,
            maximum_duration_seconds=MAXIMUM_DURATION_SECONDS,
        )

    engine = _engines[device_id]

    engine.moisture_threshold = moisture_threshold

    return engine


def get_active_watering_event(
    db: Session,
    device_id: str,
) -> Optional[WateringEvent]:
    """
    Find the currently active watering event.

    duration == 0 means the watering cycle
    has started but has not yet completed.
    """

    return (
        db.query(WateringEvent)
        .filter(
            WateringEvent.device_id == device_id,
            WateringEvent.duration == 0,
        )
        .order_by(
            WateringEvent.timestamp.desc()
        )
        .first()
    )


def calculate_water_consumption(
    duration: int,
) -> float:
    """
    Calculate virtual water consumption.
    """

    return (
        duration
        * WATER_CONSUMPTION_PER_SECOND
    )


def update_water_tank(
    device: Device,
    duration: int,
) -> float:
    """
    Decrease the virtual water tank based
    on watering duration.
    """

    consumption = calculate_water_consumption(
        duration
    )

    current_level = (
        device.water_tank_level
        if device.water_tank_level is not None
        else VIRTUAL_WATER_TANK_LEVEL
    )

    new_level = max(
        0.0,
        current_level - consumption,
    )

    device.water_tank_level = new_level

    return new_level


def complete_watering_event(
    db: Session,
    device: Device,
    event: WateringEvent,
    moisture_after: float,
    duration: int,
) -> float:
    """
    Complete a watering event and update
    the virtual water tank.
    """

    event.moisture_after = moisture_after
    event.duration = max(0, duration)

    new_tank_level = update_water_tank(
        device=device,
        duration=duration,
    )

    db.commit()

    return new_tank_level


def process_automatic_watering(
    db: Session,
    device: Device,
    soil_moisture: float,
) -> dict:
    """
    Evaluate the current sensor reading and control
    the virtual pump automatically.
    """

    engine = get_engine(
        device_id=device.device_id,
        moisture_threshold=device.moisture_threshold,
    )

    # ---------------------------------------------------------
    # CASE 1: AUTOMATIC WATERING DISABLED
    # ---------------------------------------------------------

    if not device.auto_water:
        if device.pump_status:
            return {
                "action": "PUMP_RUNNING",
                "pump_status": "ON",
                "reason": (
                    "Automatic watering is disabled, "
                    "but an existing watering cycle is running."
                ),
                "moisture": soil_moisture,
                "water_tank_level": device.water_tank_level,
            }

        return {
            "action": "NONE",
            "pump_status": "OFF",
            "reason": "Automatic watering is disabled.",
            "water_tank_level": device.water_tank_level,
        }

    # ---------------------------------------------------------
    # CASE 2: PUMP ALREADY ON
    # ---------------------------------------------------------

    if device.pump_status:

        # If the in-memory engine was lost after a restart,
        # synchronize it from the active database event.
        if not engine.pump_on:
            active_event = get_active_watering_event(
                db=db,
                device_id=device.device_id,
            )

            if active_event:
                engine.pump_on = True
                engine.pump_started_at = (
                    active_event.timestamp
                )

        should_stop = False
        stop_reason = ""

        if soil_moisture >= device.moisture_threshold:
            should_stop = True
            stop_reason = (
                "Soil moisture reached the target threshold."
            )

        elif engine.check_maximum_duration():
            should_stop = True
            stop_reason = (
                "Maximum pump duration reached."
            )

        elif (
            device.water_tank_level
            <= MINIMUM_WATER_TANK_LEVEL
        ):
            should_stop = True
            stop_reason = (
                "Virtual water tank reached the "
                "minimum safe level."
            )

        if should_stop:

            stop_result = engine.stop_pump(
                moisture_after=soil_moisture
            )

            device.pump_status = False

            duration = stop_result.get(
                "duration",
                0,
            )

            active_event = get_active_watering_event(
                db=db,
                device_id=device.device_id,
            )

            if active_event:

                new_tank_level = complete_watering_event(
                    db=db,
                    device=device,
                    event=active_event,
                    moisture_after=soil_moisture,
                    duration=duration,
                )

            else:

                fallback_event = WateringEvent(
                    device_id=device.device_id,
                    trigger_type="AUTO",
                    moisture_before=soil_moisture,
                    moisture_after=soil_moisture,
                    duration=duration,
                    timestamp=datetime.utcnow(),
                )

                db.add(fallback_event)

                new_tank_level = update_water_tank(
                    device=device,
                    duration=duration,
                )

                db.commit()

            return {
                "action": "PUMP_OFF",
                "pump_status": "OFF",
                "reason": stop_reason,
                "moisture": soil_moisture,
                "duration": duration,
                "water_consumed": calculate_water_consumption(
                    duration
                ),
                "water_tank_level": new_tank_level,
            }

        return {
            "action": "PUMP_RUNNING",
            "pump_status": "ON",
            "reason": "Pump is watering the plant.",
            "moisture": soil_moisture,
            "water_tank_level": device.water_tank_level,
        }

    # ---------------------------------------------------------
    # CASE 3: PUMP OFF AND TANK TOO LOW
    # ---------------------------------------------------------

    if (
        device.water_tank_level
        <= MINIMUM_WATER_TANK_LEVEL
    ):
        return {
            "action": "NO_WATERING",
            "pump_status": "OFF",
            "reason": (
                "Virtual water tank level is too low."
            ),
            "moisture": soil_moisture,
            "water_tank_level": device.water_tank_level,
        }

    # ---------------------------------------------------------
    # CASE 4: PUMP OFF AND SOIL IS DRY
    # ---------------------------------------------------------

    start_result = engine.start_pump(
        soil_moisture=soil_moisture,
        water_tank_level=device.water_tank_level,
    )

    if start_result["success"]:

        device.pump_status = True

        watering_event = WateringEvent(
            device_id=device.device_id,
            trigger_type="AUTO",
            moisture_before=soil_moisture,
            moisture_after=soil_moisture,
            duration=0,
            timestamp=datetime.utcnow(),
        )

        db.add(watering_event)

        db.commit()

        return {
            "action": "PUMP_ON",
            "pump_status": "ON",
            "reason": (
                "Soil moisture is below the threshold."
            ),
            "moisture": soil_moisture,
            "water_tank_level": device.water_tank_level,
        }

    return {
        "action": "NO_WATERING",
        "pump_status": "OFF",
        "reason": start_result["reason"],
        "moisture": soil_moisture,
        "water_tank_level": device.water_tank_level,
    }