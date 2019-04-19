from datetime import timedelta
from timeutils import to_hours


def get_new_interior_temperature(indoor_temperature: float,
                                 outdoor_temperature: float,
                                 open_doors: int,
                                 open_windows: int) -> float:
    temp_diff = outdoor_temperature - indoor_temperature
    temp_scale = temp_diff / 10
    if open_doors == 0 and open_windows == 0:
        CLOSED_HOUSE_RATE_CHANGE = 2 / 60
        temp_delta = CLOSED_HOUSE_RATE_CHANGE * temp_scale
    else:
        OPEN_DOOR_RATE_CHANGE = 2 / 5
        OPEN_WINDOW_RATE_CHANGE = 1 / 5
        total_door_change = OPEN_DOOR_RATE_CHANGE * open_doors
        total_window_change = OPEN_WINDOW_RATE_CHANGE * open_windows
        temp_delta = (total_door_change + total_window_change) * temp_scale
    return indoor_temperature + temp_delta


def get_new_HVAC_temperature(indoor_temperature: float,
                             preset_temperature: float) -> float:
    temp_diff = preset_temperature - indoor_temperature
    if abs(temp_diff) < 1.0:
        return indoor_temperature
    return indoor_temperature + 1 if temp_diff >= 0 else indoor_temperature - 1


def watt_hours_to_kwatt_hours(watt_hours: float) -> float:
    return watt_hours / 1000


def power_to_dollars(watt_hours: float) -> float:
    ELECTRICITY_COST_RATE = 0.12 # dollar per kWh
    power_kwh = watt_hours_to_kwatt_hours(watt_hours)
    return power_kwh * ELECTRICITY_COST_RATE;


def general_eq(rated_power: int, run_time: timedelta) -> float:
    return rated_power * to_hours(run_time)


def compute_water_heater_usage(water_required: float) -> float:
    HEATER_MIN_PER_GAL = timedelta(minutes=4)
    HEATER_RATED_POWER = 4500
    return general_eq(HEATER_RATED_POWER, water_required * HEATER_MIN_PER_GAL)
