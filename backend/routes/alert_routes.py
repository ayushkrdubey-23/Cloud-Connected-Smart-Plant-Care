from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Alert, Device
from backend.services.alert_service import check_device_offline


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"],
)


@router.get("/{device_id}")
def get_alerts(
    device_id: str,
    status: str | None = Query(default=None),
    limit: int = Query(
        default=20,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
):
    """
    Get alerts for a device.
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

    query = (
        db.query(Alert)
        .filter(Alert.device_id == device_id)
    )

    if status:
        query = query.filter(
            Alert.status == status
        )

    alerts = (
        query
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "device_id": device_id,
        "count": len(alerts),
        "alerts": [
            {
                "id": alert.id,
                "alert_type": alert.alert_type,
                "message": alert.message,
                "level": alert.level,
                "status": alert.status,
                "created_at": alert.created_at,
            }
            for alert in alerts
        ],
    }


@router.post("/{device_id}/check-offline")
def check_offline_status(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Check whether a device is offline.
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

    created = check_device_offline(
        db=db,
        device=device,
        offline_minutes=2,
    )

    return {
        "device_id": device_id,
        "offline_alert_created": created,
        "last_seen": device.last_seen,
    }


@router.patch("/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    """
    Mark an alert as acknowledged.
    """

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found.",
        )

    alert.status = "ACKNOWLEDGED"

    db.commit()
    db.refresh(alert)

    return {
        "message": "Alert acknowledged successfully.",
        "alert_id": alert.id,
        "status": alert.status,
    }