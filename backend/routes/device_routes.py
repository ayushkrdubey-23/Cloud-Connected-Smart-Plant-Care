from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Device


router = APIRouter(
    prefix="/api/devices",
    tags=["Devices"],
)


class DeviceCreate(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=50)
    plant_name: str = Field(default="My Plant", max_length=100)
    plant_type: str = Field(default="INDOOR_PLANT", max_length=50)
    location: str = Field(default="Indoor", max_length=100)


class DeviceUpdate(BaseModel):
    plant_name: str | None = Field(default=None, max_length=100)
    plant_type: str | None = Field(default=None, max_length=50)
    location: str | None = Field(default=None, max_length=100)
    moisture_threshold: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )
    auto_water: bool | None = None


@router.get("")
def get_devices(
    db: Session = Depends(get_db),
):
    """
    Get all registered devices.
    """

    devices = (
        db.query(Device)
        .order_by(Device.created_at.desc())
        .all()
    )

    return {
        "count": len(devices),
        "devices": [
            {
                "device_id": device.device_id,
                "plant_name": device.plant_name,
                "plant_type": device.plant_type,
                "location": device.location,
                "moisture_threshold": device.moisture_threshold,
                "pump_status": device.pump_status,
                "auto_water": device.auto_water,
                "water_tank_level": device.water_tank_level,
                "last_seen": device.last_seen,
                "created_at": device.created_at,
            }
            for device in devices
        ],
    }


@router.post("")
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new plant device.
    """

    existing = (
        db.query(Device)
        .filter(Device.device_id == data.device_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Device already exists.",
        )

    device = Device(
        device_id=data.device_id,
        plant_name=data.plant_name,
        plant_type=data.plant_type.upper(),
        location=data.location,
        moisture_threshold=30.0,
        pump_status=False,
        auto_water=True,
        water_tank_level=100.0,
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return {
        "message": "Device created successfully.",
        "device": {
            "device_id": device.device_id,
            "plant_name": device.plant_name,
            "plant_type": device.plant_type,
            "location": device.location,
            "moisture_threshold": device.moisture_threshold,
            "pump_status": device.pump_status,
            "auto_water": device.auto_water,
            "water_tank_level": device.water_tank_level,
        },
    }


@router.get("/{device_id}")
def get_device(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Get details of a specific device.
    """

    device = (
        db.query(Device)
        .filter(Device.device_id == device_id)
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
        "location": device.location,
        "moisture_threshold": device.moisture_threshold,
        "pump_status": device.pump_status,
        "auto_water": device.auto_water,
        "water_tank_level": device.water_tank_level,
        "last_seen": device.last_seen,
        "created_at": device.created_at,
    }


@router.put("/{device_id}")
def update_device(
    device_id: str,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
):
    """
    Update plant/device settings.
    """

    device = (
        db.query(Device)
        .filter(Device.device_id == device_id)
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found.",
        )

    if data.plant_name is not None:
        device.plant_name = data.plant_name

    if data.plant_type is not None:
        device.plant_type = data.plant_type.upper()

    if data.location is not None:
        device.location = data.location

    if data.moisture_threshold is not None:
        device.moisture_threshold = data.moisture_threshold

    if data.auto_water is not None:
        device.auto_water = data.auto_water

    db.commit()
    db.refresh(device)

    return {
        "message": "Device updated successfully.",
        "device": {
            "device_id": device.device_id,
            "plant_name": device.plant_name,
            "plant_type": device.plant_type,
            "location": device.location,
            "moisture_threshold": device.moisture_threshold,
            "pump_status": device.pump_status,
            "auto_water": device.auto_water,
            "water_tank_level": device.water_tank_level,
        },
    }