import datetime as dt

# Module with some miscellaneous utilities

# Transform teh input date by user (integer in format YYYYMMDD) to DateTime
def int_to_date(integer):
    if integer is None:
        return dt.datetime.utcnow()

    date_string = str(integer)
    date_time = dt.datetime.strptime(date_string, "%Y%m%d")
    date_time_string = date_time.isoformat()
    return date_time_string

# Get the final date based on "ndays" informed by user
def get_final_date(initial_date, delta):

    if initial_date == None:
        date_obj = dt.datetime.utcnow()
    else:
        date_obj = dt.datetime.strptime(str(initial_date), '%Y%m%d')

    final_date_obj = date_obj + dt.timedelta(days=delta)
    print(final_date_obj)
    return final_date_obj.strftime('%Y-%m-%d')

# List of valid measures. If user enter a different measure, it will raise an exception
valid_measures = ['temperature', 'humidity', 'dew_point', 'pressure', 'wind', 'cloud_cover']
