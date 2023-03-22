# The Meteomatics free trial license accepts a limit of 10 parameters per request

#parameter example: "t_0m:C"
temperature = 't'
temperature_levels = ['_2m', '_10m', '_1000hPa']
temperature_units = ['C', 'F', 'K']

#parameter example: "relative_humidity_1000hPa:p"
humidity = 'relative_humidity'
humidity_levels = ['_2m', '_10m', '_1000hPa']
humidity_units = ['p']

dew_point = 'dew_point'
dew_point_levels = ['_2m', '_10m', '_1000hPa']
dew_point_units = ['C', 'F', 'K']

# Pressure does not accept levels
#parameter example:" msl_pressure:hPa"
pressure = 'msl_pressure'
pressure_units = ['Pa', 'hPa', 'psi']

wind_speed = 'wind_speed'
wind_speed_levels = ['_2m', '_5ft', '_1000hPa']
wind_speed_units = ['kmh', 'ms', 'mph', 'kn', 'bft']

wind_dir = 'wind_dir'
wind_dir_levels = ['_2m:d', '_5ft:d', '_1000hPa:d']

# Cloud cover levels come before the constant
cloud_cover = 'cloud_cover'
cloud_cover_levels = ['low_', 'medium_', 'high_']
cloud_cover_units = ['octas', 'p']

# Dictionary with all measures that we will be working with, including constants, levels and units
parameters_dictionary = {
    'temperature': {
        'constant': temperature,
        'levels': temperature_levels,
        'units': temperature_units
    },
    'humidity':{
        'constant': humidity,
        'levels': humidity_levels,
        'units': humidity_units
    },
    'dew_point': {
        'constant': dew_point,
        'levels': dew_point_levels,
        'units': dew_point_units
    },
    'pressure': {
        'constant': pressure,
        'levels': None,
        'units': pressure_units
    },
    'wind_speed': {
        'constant': wind_speed,
        'levels': wind_speed_levels,
        'units': wind_speed_units
    },
    'wind_dir': {
        'constant': wind_dir,
        'levels': wind_dir_levels,
        'units': None
    },
    'cloud_cover': {
        'constant': cloud_cover,
        'levels': cloud_cover_levels,
        'units': cloud_cover_units
    }

}
