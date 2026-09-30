PLANT_PROFILES = {
    "SUCCULENT": {
        "moisture_threshold": 20.0,
        "description": "Requires relatively dry soil."
    },

    "TOMATO": {
        "moisture_threshold": 40.0,
        "description": "Requires moderate soil moisture."
    },

    "HERB": {
        "moisture_threshold": 35.0,
        "description": "Requires consistently moist soil."
    },

    "INDOOR_PLANT": {
        "moisture_threshold": 30.0,
        "description": "Moderate moisture requirement."
    }
}


def get_plant_profile(
    plant_type: str
) -> dict:
    """
    Return the configured profile for a plant.
    """

    plant_type = plant_type.upper()

    return PLANT_PROFILES.get(
        plant_type,
        PLANT_PROFILES["INDOOR_PLANT"]
    )


def get_moisture_threshold(
    plant_type: str
) -> float:
    """
    Return moisture threshold for a plant.
    """

    profile = get_plant_profile(
        plant_type
    )

    return profile["moisture_threshold"]