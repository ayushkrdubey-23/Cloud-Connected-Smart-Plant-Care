from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    plant_name = Column(
        String,
        nullable=False
    )

    plant_type = Column(
        String,
        nullable=False
    )

    location = Column(
        String,
        default="Indoor"
    )

    moisture_threshold = Column(
        Float,
        default=30.0
    )

    pump_status = Column(
        Boolean,
        default=False
    )

    auto_water = Column(
        Boolean,
        default=True
    )

    # Virtual water tank level.
    # Value is stored as a percentage from 0 to 100.
    water_tank_level = Column(
        Float,
        default=100.0
    )

    last_seen = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    device_id = Column(
        String,
        index=True,
        nullable=False
    )

    soil_moisture = Column(
        Float,
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=False
    )

    humidity = Column(
        Float,
        nullable=False
    )

    light_level = Column(
        Float,
        nullable=False
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )


class WateringEvent(Base):
    __tablename__ = "watering_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    device_id = Column(
        String,
        index=True,
        nullable=False
    )

    trigger_type = Column(
        String,
        nullable=False
    )

    moisture_before = Column(
        Float,
        nullable=True
    )

    moisture_after = Column(
        Float,
        nullable=True
    )

    duration = Column(
        Integer,
        default=0
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    device_id = Column(
        String,
        index=True,
        nullable=False
    )

    alert_type = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    level = Column(
        String,
        default="INFO"
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )