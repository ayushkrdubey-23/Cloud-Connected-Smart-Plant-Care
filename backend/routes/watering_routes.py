from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Device, SensorReading, WateringEvent
from backend.services.watering_service import (
    MINIMUM_WATER_TANK_LEVEL,
    VIRTUAL_WATER_TANK_LEVEL,
    get_engine,
)


router = APIRouter(
    prefix="/api/watering",
    tags=["Watering"],
)


@router.post("/{device_id}/manual")
def manual_watering(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Manually start the virtual water pump.

    Manual watering is an explicit user action, so it
    can operate even when soil moisture is above the
    automatic watering threshold.
    """

    device = (
        db.query(Device)
        .filter(
            Device.device_id == device_id
        )
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found.",
        )

    if device.pump_status:
        raise HTTPException(
            status_code=409,
            detail="Virtual pump is already running.",
        )

    current_tank_level = (
        device.water_tank_level
        if device.water_tank_level is not None
        else VIRTUAL_WATER_TANK_LEVEL
    )

    if current_tank_level <= MINIMUM_WATER_TANK_LEVEL:
        raise HTTPException(
            status_code=409,
            detail=(
                "Virtual water tank level is too low "
                "for manual watering."
            ),
        )

    latest_reading = (
        db.query(SensorReading)
        .filter(
            SensorReading.device_id == device_id
        )
        .order_by(
            SensorReading.timestamp.desc()
        )
        .first()
    )

    if latest_reading:
        moisture_before = latest_reading.soil_moisture
    else:
        moisture_before = 0.0

    engine = get_engine(
        device_id=device_id,
        moisture_threshold=device.moisture_threshold,
    )

    if engine.pump_on:
        raise HTTPException(
            status_code=409,
            detail="Virtual pump is already running.",
        )

    # Start the virtual pump directly because this
    # is an explicit manual watering request.
    engine.pump_on = True
    engine.pump_started_at = datetime.utcnow()

    device.pump_status = True

    event = WateringEvent(
        device_id=device_id,
        trigger_type="MANUAL",
        moisture_before=moisture_before,
        moisture_after=moisture_before,
        duration=0,
        timestamp=datetime.utcnow(),
    )

    db.add(event)
    db.commit()

    db.refresh(event)
    db.refresh(device)

    return {
        "success": True,
        "message": "Manual watering started successfully.",
        "device_id": device_id,
        "pump_status": "ON",
        "trigger_type": "MANUAL",
        "moisture_before": moisture_before,
        "watering_event_id": event.id,
        "water_tank_level": device.water_tank_level,
        "timestamp": event.timestamp,
    }


@router.post("/{device_id}/refill")
def refill_water_tank(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Refill the virtual water tank to 100%.

    This simulates physically refilling the water
    container connected to the virtual plant system.
    """

    device = (
        db.query(Device)
        .filter(
            Device.device_id == device_id
        )
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found.",
        )

    if device.pump_status:
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot refill the water tank while "
                "the virtual pump is running."
            ),
        )

    previous_level = (
        device.water_tank_level
        if device.water_tank_level is not None
        else VIRTUAL_WATER_TANK_LEVEL
    )

    device.water_tank_level = VIRTUAL_WATER_TANK_LEVEL

    db.commit()
    db.refresh(device)

    return {
        "success": True,
        "message": "Virtual water tank refilled successfully.",
        "device_id": device_id,
        "previous_water_tank_level": previous_level,
        "water_tank_level": device.water_tank_level,
        "unit": "percent",
        "pump_status": "OFF",
        "timestamp": datetime.utcnow(),
    }


@router.get("/{device_id}/history")
def get_watering_history(
    device_id: str,
    limit: int = Query(
        default=20,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
):
    """
    Get watering history for a device.
    """

    device = (
        db.query(Device)
        .filter(
            Device.device_id == device_id
        )
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found.",
        )

    events = (
        db.query(WateringEvent)
        .filter(
            WateringEvent.device_id == device_id
        )
        .order_by(
            WateringEvent.timestamp.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "device_id": device_id,
        "count": len(events),
        "history": [
            {
                "id": event.id,
                "trigger_type": event.trigger_type,
                "moisture_before": event.moisture_before,
                "moisture_after": event.moisture_after,
                "duration": event.duration,
                "timestamp": event.timestamp,
            }
            for event in events
        ],
    }