from automation.watering_engine import WateringEngine


def test_watering_when_soil_is_dry():
    engine = WateringEngine(
        moisture_threshold=40
    )

    result = engine.start_pump(
        soil_moisture=25,
        water_tank_level=100
    )

    assert result["success"] is True
    assert result["pump_status"] == "ON"


def test_no_watering_when_soil_is_wet():
    engine = WateringEngine(
        moisture_threshold=40
    )

    result = engine.start_pump(
        soil_moisture=60,
        water_tank_level=100
    )

    assert result["success"] is False
    assert result["pump_status"] == "OFF"


def test_no_watering_when_tank_is_empty():
    engine = WateringEngine(
        moisture_threshold=40
    )

    result = engine.start_pump(
        soil_moisture=20,
        water_tank_level=5
    )

    assert result["success"] is False
    assert result["pump_status"] == "OFF"


def test_pump_can_stop():
    engine = WateringEngine(
        moisture_threshold=40
    )

    start_result = engine.start_pump(
        soil_moisture=20,
        water_tank_level=100
    )

    assert start_result["pump_status"] == "ON"

    stop_result = engine.stop_pump(
        moisture_after=50
    )

    assert stop_result["success"] is True
    assert stop_result["pump_status"] == "OFF"
    