import os

from dotenv import load_dotenv


# Load .env from the project root.
load_dotenv()


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)

DEVICE_ID = os.getenv(
    "DEVICE_ID",
    "PLANT-001",
)

SIMULATOR_INTERVAL = int(
    os.getenv(
        "SIMULATOR_INTERVAL",
        "5",
    )
)

OFFLINE_MODE = (
    os.getenv(
        "OFFLINE_MODE",
        "false",
    ).lower()
    == "true"
)

REQUEST_TIMEOUT = float(
    os.getenv(
        "REQUEST_TIMEOUT",
        "5",
    )
)

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "3",
    )
)