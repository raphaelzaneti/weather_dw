import meteomatics.api as api
import datetime as dt
from local_settings import meteomatics_credentials as cred
from utils.parameters_dict import parameters_dictionary
from data_storage.update_db import parse_location
import pandas as pd

def call_met(lat, long, days_qty, weather_params):

    parameters = []
    if weather_params == ['wind']:
        weather_params = ['wind_speed', 'wind_dir']
    # Based on user measure input, it get the parameters name according to Meteomatics API documentation
    # There is a HTTP excemption handling to prevent the user to send invalid measures
    for param in weather_params:
        if parameters_dictionary[param]['levels'] != None:
            for level in parameters_dictionary[param]['levels']:
                unit = ":"+parameters_dictionary[param]['units'][0] if parameters_dictionary[param]['units'] is not None else ""
                if param == "cloud_cover": # Special case for cloud_cover measure, as for this one the level come before the constant
                    parameters.append(f'{level}{parameters_dictionary[param]["constant"]}{unit}')
                else:
                    parameters.append(f'{parameters_dictionary[param]["constant"]}{level}{unit}')

    # Username and password to access the DB are saved in a private file
    username = cred['username']
    password = cred['password']

    coords = [(lat, long)]

    # Due to the free trial API license, the startdate is limited. So we will be using, as default, the current date/time
    startdate = dt.datetime.utcnow().replace(hour=1, minute=0, second=0, microsecond=0)
    enddate = startdate+dt.timedelta(days=days_qty)

    interval = dt.timedelta(hours=1)

    # Get the output from Meteomatics and store it into a dataframe
    df = pd.DataFrame(api.query_time_series(coords, startdate, enddate, interval, parameters, username, password))

    # Reset the indexes of the DF to get lat, lon and date
    df = df.reset_index()
    df = df.rename(columns={'lat': 'lat', 'lon': 'lon', 'validdate': 'validdate'})

    # Transform DF to dictionary
    df_dict = df.to_dict(orient='list')
    parse_location(df_dict)