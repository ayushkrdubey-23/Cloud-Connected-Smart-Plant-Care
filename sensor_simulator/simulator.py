import logging
import math
import random
import time
from datetime import datetime

import httpx

from sensor_simulator.config import (
    API_URL,
    DEVICE_ID,
    SIMULATOR_INTERVAL,
    OFFLINE_MODE,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


soil_moisture = 55.0
temperature = 27.0
humidity = 60.0


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def get_pump_status() -> bool:
    """
    Check whether the backend virtual pump is ON.
    """

    url = f"{API_URL}/api/sensors/{DEVICE_ID}/status"

    try:
        response = httpx.get(
            url,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("pump_status", False)

    except httpx.RequestError as exc:
        logger.warning("Could not read pump status: %s", exc)

    return False


def simulate_soil_moisture(pump_on: bool) -> float:
    """
    Simulate realistic soil moisture.

    Pump OFF:
        Moisture gradually decreases.

    Pump ON:
        Moisture gradually increases.
    """

    global soil_moisture

    if pump_on:
        change = random.uniform(2.5, 4.5)
        soil_moisture += change
    else:
        change = random.uniform(0.7, 1.5)
        soil_moisture -= change

    soil_moisture = clamp(
        soil_moisture,
        5.0,
        95.0,
    )

    return round(soil_moisture, 2)


def simulate_temperature() -> float:
    """
    Simulate gradual temperature changes.
    """

    global temperature

    temperature += random.uniform(-0.3, 0.3)

    temperature = clamp(
        temperature,
        20.0,
        38.0,
    )

    return round(temperature, 2)


def simulate_humidity() -> float:
    """
    Simulate gradual humidity changes.
    """

    global humidity

    humidity += random.uniform(-1.0, 1.0)

    humidity = clamp(
        humidity,
        35.0,
        85.0,
    )

    return round(humidity, 2)


def simulate_light() -> float:
    """
    Simulate day/night light using a sine wave.
    """

    hour = datetime.now().hour

    angle = ((hour - 6) / 12) * math.pi

    light = max(
        0,
        math.sin(angle),
    )

    light += random.uniform(-0.05, 0.05)

    light = clamp(
        light * 100,
        0,
        100,
    )

    return round(light, 2)


def create_sensor_payload() -> dict:
    """
    Create a complete sensor payload.
    """

    pump_on = get_pump_status()

    moisture = simulate_soil_moisture(
        pump_on=pump_on
    )

    payload = {
        "device_id": DEVICE_ID,
        "soil_moisture": moisture,
        "temperature": simulate_temperature(),
        "humidity": simulate_humidity(),
        "light_level": simulate_light(),
        "timestamp": datetime.utcnow().isoformat(),
    }

    logger.info(
        "Sensors | moisture=%.2f%% | temperature=%.2f°C | humidity=%.2f%% | pump=%s",
        payload["soil_moisture"],
        payload["temperature"],
        payload["humidity"],
        payload["pump_status"] if "pump_status" in payload else pump_on,
    )

    return payload


def send_sensor_data(payload: dict) -> bool:
    """
    Send sensor data to the FastAPI backend.
    """

    if OFFLINE_MODE:
        logger.info(
            "OFFLINE MODE | Sensor data generated but not sent: %s",
            payload,
        )
        return True

    url = f"{API_URL}/api/sensors/data"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = httpx.post(
                url,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code == 200:
                result = response.json()

                watering = result.get(
                    "watering",
                    {},
                )

                logger.info(
                    "Backend | action=%s | pump=%s | reason=%s",
                    watering.get("action"),
                    watering.get("pump_status"),
                    watering.get("reason"),
                )

                return True

            logger.warning(
                "Backend returned HTTP %s: %s",
                response.status_code,
                response.text,
            )

        except httpx.RequestError as exc:
            logger.warning(
                "Request failed (attempt %s/%s): %s",
                attempt,
                MAX_RETRIES,
                exc,
            )

        if attempt < MAX_RETRIES:
            time.sleep(1)

    return False


def main():
    logger.info("=" * 60)
    logger.info("Cloud-Connected Smart Plant Care")
    logger.info("Virtual IoT Sensor Simulator")
    logger.info("=" * 60)

    logger.info("Device ID: %s", DEVICE_ID)
    logger.info("API URL: %s", API_URL)
    logger.info("Interval: %s seconds", SIMULATOR_INTERVAL)
    logger.info("Offline mode: %s", OFFLINE_MODE)

    while True:
        try:
            payload = create_sensor_payload()

            success = send_sensor_data(payload)

            if success:
                logger.info(
                    "Sensor cycle completed successfully."
                )
            else:
                logger.warning(
                    "Sensor cycle failed."
                )

            time.sleep(SIMULATOR_INTERVAL)

        except KeyboardInterrupt:
            logger.info(
                "Sensor simulator stopped by user."
            )
            break

        except Exception as exc:
            logger.exception(
                "Unexpected simulator error: %s",
                exc,
            )
            time.sleep(SIMULATOR_INTERVAL)


if __name__ == "__main__":
    main()