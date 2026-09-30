from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Device, SensorReading
from backend.services.alert_service import evaluate_sensor_alerts
from backend.services.watering_service import process_automatic_watering


router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"],
)


class SensorData(BaseModel):
    device_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    soil_moisture: float = Field(
        ...,
        ge=0,
        le=100,
    )

    temperature: float = Field(
        ...,
        ge=-20,
        le=60,
    )

    humidity: float = Field(
        ...,
        ge=0,
        le=100,
    )

    light_level: float = Field(
        ...,
        ge=0,
        le=100,
    )

    timestamp: Optional[datetime] = None


@router.post("/data")
def receive_sensor_data(
    data: SensorData,
    db: Session = Depends(get_db),
):
    """
    Receive sensor data, process watering,
    and generate alerts.
    """

    device = (
        db.query(Device)
        .filter(
            Device.device_id == data.device_id
        )
        .first()
    )

    # ---------------------------------------------------------
    # CREATE DEMO DEVICE IF IT DOES NOT EXIST
    # ---------------------------------------------------------

    if not device:
        device = Device(
            device_id=data.device_id,
            plant_name="Tomato Plant",
            plant_type="TOMATO",
            location="Indoor",
            moisture_threshold=40.0,
            pump_status=False,
            auto_water=True,
            water_tank_level=100.0,
        )

        db.add(device)
        db.commit()
        db.refresh(device)

    # ---------------------------------------------------------
    # SAVE SENSOR READING
    # ---------------------------------------------------------

    reading = SensorReading(
        device_id=data.device_id,
        soil_moisture=data.soil_moisture,
        temperature=data.temperature,
        humidity=data.humidity,
        light_level=data.light_level,
        timestamp=data.timestamp or datetime.utcnow(),
    )

    db.add(reading)

    device.last_seen = datetime.utcnow()

    db.commit()

    # ---------------------------------------------------------
    # AUTOMATIC WATERING
    # ---------------------------------------------------------

    watering_result = process_automatic_watering(
        db=db,
        device=device,
        soil_moisture=data.soil_moisture,
    )

    # ---------------------------------------------------------
    # SENSOR ALERTS
    # ---------------------------------------------------------

    alert_types = evaluate_sensor_alerts(
        db=db,
        device=device,
        soil_moisture=data.soil_moisture,
        temperature=data.temperature,
        water_tank_level=device.water_tank_level,
    )

    db.refresh(device)

    return {
        "message": "Sensor data received successfully.",
        "device_id": data.device_id,

        "reading": {
            "soil_moisture": data.soil_moisture,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "light_level": data.light_level,
        },

        "watering": watering_result,

        "water_tank": {
            "level": device.water_tank_level,
            "unit": "percent",
        },

        "alerts": {
            "created": alert_types,
            "count": len(alert_types),
        },

        "device": {
            "pump_status": device.pump_status,
            "auto_water": device.auto_water,
            "moisture_threshold": device.moisture_threshold,
            "water_tank_level": device.water_tank_level,
        },
    }


@router.get("/{device_id}/latest")
def get_latest_sensor_reading(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Get the latest sensor reading for a device.
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

    reading = (
        db.query(SensorReading)
        .filter(
            SensorReading.device_id == device_id
        )
        .order_by(
            SensorReading.timestamp.desc()
        )
        .first()
    )

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="No sensor reading found.",
        )

    return {
        "device_id": device_id,
        "soil_moisture": reading.soil_moisture,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "light_level": reading.light_level,
        "timestamp": reading.timestamp,
    }


@router.get("/{device_id}/history")
def get_sensor_history(
    device_id: str,
    limit: int = Query(
        default=20,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
):
    """
    Get recent sensor history.
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

    readings = (
        db.query(SensorReading)
        .filter(
            SensorReading.device_id == device_id
        )
        .order_by(
            SensorReading.timestamp.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "device_id": device_id,
        "count": len(readings),
        "history": [
            {
                "id": reading.id,
                "soil_moisture": reading.soil_moisture,
                "temperature": reading.temperature,
                "humidity": reading.humidity,
                "light_level": reading.light_level,
                "timestamp": reading.timestamp,
            }
            for reading in reversed(readings)
        ],
    }


@router.get("/{device_id}/status")
def get_device_status(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Get the current device status.
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

    return {
        "device_id": device.device_id,
        "plant_name": device.plant_name,
        "plant_type": device.plant_type,
        "moisture_threshold": device.moisture_threshold,
        "pump_status": device.pump_status,
        "auto_water": device.auto_water,
        "water_tank_level": device.water_tank_level,
        "last_seen": device.last_seen,
    }