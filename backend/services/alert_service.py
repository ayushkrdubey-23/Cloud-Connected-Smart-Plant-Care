from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.models import Alert, Device


def create_alert_if_needed(
    db: Session,
    device: Device,
    alert_type: str,
    message: str,
    level: str,
) -> bool:
    """
    Create an alert only when a similar active alert
    does not already exist.
    """

    existing_alert = (
        db.query(Alert)
        .filter(
            Alert.device_id == device.device_id,
            Alert.alert_type == alert_type,
            Alert.status == "ACTIVE",
        )
        .first()
    )

    if existing_alert:
        return False

    alert = Alert(
        device_id=device.device_id,
        alert_type=alert_type,
        message=message,
        level=level,
        status="ACTIVE",
        created_at=datetime.utcnow(),
    )

    db.add(alert)
    db.commit()

    return True


def evaluate_sensor_alerts(
    db: Session,
    device: Device,
    soil_moisture: float,
    temperature: float,
    water_tank_level: float = 100.0,
):
    """
    Evaluate sensor readings and create alerts.
    """

    created_alerts = []

    # ---------------------------------------------------------
    # LOW SOIL MOISTURE
    # ---------------------------------------------------------
    if soil_moisture < 20:
        created = create_alert_if_needed(
            db=db,
            device=device,
            alert_type="LOW_MOISTURE",
            message=(
                f"Soil moisture is critically low at "
                f"{soil_moisture:.1f}%."
            ),
            level="CRITICAL",
        )

        if created:
            created_alerts.append("LOW_MOISTURE")

    elif soil_moisture < device.moisture_threshold:
        created = create_alert_if_needed(
            db=db,
            device=device,
            alert_type="LOW_MOISTURE",
            message=(
                f"Soil moisture is below the target "
                f"threshold at {soil_moisture:.1f}%."
            ),
            level="WARNING",
        )

        if created:
            created_alerts.append("LOW_MOISTURE")

    # ---------------------------------------------------------
    # HIGH TEMPERATURE
    # ---------------------------------------------------------
    if temperature > 35:
        created = create_alert_if_needed(
            db=db,
            device=device,
            alert_type="HIGH_TEMPERATURE",
            message=(
                f"Temperature is high at "
                f"{temperature:.1f}°C."
            ),
            level="WARNING",
        )

        if created:
            created_alerts.append("HIGH_TEMPERATURE")

    # ---------------------------------------------------------
    # LOW WATER TANK
    # ---------------------------------------------------------
    if water_tank_level <= 10:
        created = create_alert_if_needed(
            db=db,
            device=device,
            alert_type="LOW_WATER_TANK",
            message=(
                f"Water tank level is low at "
                f"{water_tank_level:.1f}%."
            ),
            level="CRITICAL",
        )

        if created:
            created_alerts.append("LOW_WATER_TANK")

    return created_alerts


def check_device_offline(
    db: Session,
    device: Device,
    offline_minutes: int = 2,
):
    """
    Check whether a device has stopped sending sensor data.
    """

    if device.last_seen is None:
        return False

    offline_limit = datetime.utcnow() - timedelta(
        minutes=offline_minutes
    )

    if device.last_seen < offline_limit:
        return create_alert_if_needed(
            db=db,
            device=device,
            alert_type="DEVICE_OFFLINE",
            message=(
                f"Device has not sent data for more than "
                f"{offline_minutes} minutes."
            ),
            level="WARNING",
        )

    return False