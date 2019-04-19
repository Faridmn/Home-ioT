from datetime import timedelta
from calculate import general_eq, compute_water_heater_usage

device_types = [
    ('Door', 'DOOR'),
    ('Window', 'WINDOW'),
    ('Bulb', 'BULB'),
    ('Fan', 'FAN'),
    ('Refrigerator', 'REFRIGERATOR'),
    ('Microwave', 'MICROWAVE'),
    ('Stove', 'STOVE'),
    ('Oven', 'OVEN'),
    ('Big TV', 'BIG TV'),
    ('Small TV', 'SMALL TV'),
    ('Water Heater', 'WATER HEATER'),
    ('Bath', 'BATH'),
    ('Shower', 'SHOWER'),
    ('Dishwasher', 'DISHWASHER'),
    ('Clothes Washer', 'CLOTHES WASHER'),
    ('Clothes Dryer', 'CLOTHES DRYER')
]


def get_power_and_water_usage(for_given_type: str) -> (int, int):
    #TODO: Make sure we're correctly thinking of which unit water usage is in
    #NOTE: Watt-hours and gallons?
    device_map = {
        'DOOR' : (0, 0),
        'BULB' : (60, 0),
        'WINDOW' : (0, 0),
        'FAN' : (30, 0),
        'REFRIGERATOR' : (150, 0),
        'MICROWAVE' : (1100, 0),
        'STOVE' : (3500, 0),
        'OVEN' : (4000, 0),
        'BIG TV' : (636, 0),
        'SMALL TV' : (100, 0),
        'WATER HEATER' : (4500, 0),
        'BATH' : (0, 30),
        'SHOWER' : (0, 25),
        'DISHWASHER' : (1800, 6),
        'CLOTHES WASHER' : (500, 20),
        'CLOTHES DRYER' : (3000, 0)
    }
    return device_map[for_given_type]


#def calculate_device_usage(for_given_type):
def compute_usage(device_type: str, rated_power: int, runtime: timedelta) -> dict:
    assert len(list(filter(lambda x: device_type == x[1], device_types)))
    power_used = water_used = heater_power = 0
    if device_type == 'DISHWASHER':
        water_used = 6
        hot_ratio = 1
        power_used = general_eq(rated_power, runtime)
        heater_power = compute_water_heater_usage(water_used * hot_ratio)
    elif device_type == 'CLOTHES WASHER':
        water_used = 20
        hot_ratio = 0.85
        heater_power = compute_water_heater_usage(water_used * hot_ratio)
        power_used = general_eq(rated_power, runtime)
    elif device_type == 'SHOWER':
        water_used = 25
        hot_ratio = 0.65
        heater_power = compute_water_heater_usage(water_used * hot_ratio)
    elif device_type == 'BATH':
        water_used = 30
        hot_ratio = 0.65
        heater_power = compute_water_heater_usage(water_used * hot_ratio)
    else:
        power_used = general_eq(rated_power, runtime)

    #NOTE: maybe split these up again if we need it
    return {'power': power_used + heater_power, 'water': water_used}
