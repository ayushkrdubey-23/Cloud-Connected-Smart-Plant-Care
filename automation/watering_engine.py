from datetime import datetime, timedelta


class WateringEngine:
    """
    Automated watering decision engine.

    This class determines when a virtual pump
    should be activated.
    """

    def __init__(
        self,
        moisture_threshold: float = 40.0,
        minimum_water_tank: float = 10.0,
        cooldown_minutes: int = 2,
        maximum_duration_seconds: int = 10
    ):
        self.moisture_threshold = (
            moisture_threshold
        )

        self.minimum_water_tank = (
            minimum_water_tank
        )

        self.cooldown_minutes = (
            cooldown_minutes
        )

        self.maximum_duration_seconds = (
            maximum_duration_seconds
        )

        self.pump_on = False

        self.last_watered_at = None

        self.pump_started_at = None

    def can_water(
        self,
        soil_moisture: float,
        water_tank_level: float
    ) -> tuple[bool, str]:
        """
        Determine whether watering is allowed.
        """

        if soil_moisture >= self.moisture_threshold:
            return (
                False,
                "Soil moisture is above threshold."
            )

        if water_tank_level <= self.minimum_water_tank:
            return (
                False,
                "Water tank level is too low."
            )

        if self.pump_on:
            return (
                False,
                "Pump is already running."
            )

        if self.last_watered_at is not None:

            cooldown_end = (
                self.last_watered_at
                + timedelta(
                    minutes=self.cooldown_minutes
                )
            )

            if datetime.utcnow() < cooldown_end:
                return (
                    False,
                    "Watering cooldown is active."
                )

        return (
            True,
            "Watering conditions satisfied."
        )

    def start_pump(
        self,
        soil_moisture: float,
        water_tank_level: float
    ) -> dict:
        """
        Attempt to activate the virtual pump.
        """

        allowed, reason = self.can_water(
            soil_moisture,
            water_tank_level
        )

        if not allowed:

            return {
                "success": False,
                "pump_status": "OFF",
                "reason": reason
            }

        self.pump_on = True

        self.pump_started_at = (
            datetime.utcnow()
        )

        return {
            "success": True,
            "pump_status": "ON",
            "reason": reason,
            "started_at": self.pump_started_at
        }

    def stop_pump(
        self,
        moisture_after: float
    ) -> dict:
        """
        Turn the virtual pump off.
        """

        if not self.pump_on:

            return {
                "success": False,
                "pump_status": "OFF",
                "reason": "Pump is already off."
            }

        stopped_at = datetime.utcnow()

        duration = 0

        if self.pump_started_at is not None:

            duration = int(
                (
                    stopped_at
                    - self.pump_started_at
                ).total_seconds()
            )

        self.pump_on = False

        self.last_watered_at = stopped_at

        self.pump_started_at = None

        return {
            "success": True,
            "pump_status": "OFF",
            "moisture_after": moisture_after,
            "duration": duration,
            "stopped_at": stopped_at
        }

    def check_maximum_duration(self) -> bool:
        """
        Check whether the pump has exceeded
        its maximum allowed runtime.
        """

        if not self.pump_on:
            return False

        if self.pump_started_at is None:
            return False

        elapsed = (
            datetime.utcnow()
            - self.pump_started_at
        ).total_seconds()

        return (
            elapsed
            >= self.maximum_duration_seconds
        )