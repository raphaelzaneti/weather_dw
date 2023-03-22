from sqlalchemy import Table, MetaData,  and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data_storage.db import get_engine
from data_storage.setup_db import Location, Landing, Temperature, Humidity, Dew, Pressure, Wind, Cloud
import datetime as dt

# Check if the location already exists in DB
# If yes, get id and go ahead
# If not, add it to DB, get id and go ahead
def parse_location(dict):
    add_to_landing(dict)
    location_exists = None
    location_lon = dict['lon'][0]
    location_lat = dict['lat'][0]
    metadata = MetaData()
    engine = get_engine()
    location_table = Table('location', metadata, autoload_with=engine)

    select_statement = location_table.select().where(
        and_(
            location_table.c.lon == location_lon, location_table.c.lat == location_lat
        )
    )

    with engine.connect() as conn:
        result = conn.execute(select_statement).fetchall()
        if len(result) > 0:
            location_id = result[0][0]
            location_exists = True
        else:
            location_exists = False

    if location_exists is False:
        add_location(location_lat, location_lon)
        with engine.connect() as conn:
            result = conn.execute(select_statement).fetchall()
            location_id = result[0][0]

    add_data(dict, location_id)

# Function to add a new location to DB
def add_location(lat, lon, caption=None):
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
    session = Session()

    new_location = Location(lat=lat, lon=lon, caption=caption)

    session.add(new_location)

    session.commit()
    session.close()


# Function to add any Meteomatics call to a landing table, without any transforming
def add_to_landing(dict):
    location_lon = dict['lon'][0]
    location_lat = dict['lat'][0]
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    Base = declarative_base()

    session = Session()

    cols = list(dict.keys())
    for (i, el) in enumerate(dict[cols[0]]):
        for key, values in dict.items():
            if key not in ['lat', 'lon', 'validdate']:
                new_record = Landing(
                    lat = location_lat,
                    lon = location_lon,
                    requested_at = dt.datetime.utcnow(),
                    date_value = dict['validdate'][i],
                    parameter = key.split(':')[0],
                    value = values[i],
                    unit = key.split(':')[1]
                )
                session.add(new_record)


    session.commit()
    session.close()


def add_data(dict, location_id):
    cols = list(dict.keys())
    keywords = {'t_2m': Temperature,
                'humidity': Humidity,
                'dew_point': Dew,
                'pressure': Pressure,
                'wind': Wind,
                'cloud': Cloud
                }
    tables_to_update = []
    for word in keywords.keys():
        for param in cols:
            if word in param:
                tables_to_update.append(word)
                break

    engine = get_engine()
    Session = sessionmaker(bind=engine)
    Base = declarative_base()

    session = Session()

    for (i, el) in enumerate(dict[cols[0]]):
        if 't_2m' in tables_to_update:

            is_temperature = False

            # This second validation is important, because "dew_point" will pass the first one
            for el in tables_to_update:
                if el == 't_2m':
                    is_temperature = True

            if is_temperature == True:
                for col in ['t_2m:C', 't_10m:C', 't_1000hPa:C']:
                    new_record = Temperature(
                        location_id=location_id,
                        date=dict['validdate'][i].date(),
                        time=dict['validdate'][i].time(),
                        value=dict[col][i],
                        level=col.split("_")[-1].split(":")[0],
                        unit=col.split(":")[-1]
                    )

                    session.add(new_record)

        if 'humidity' in tables_to_update:
            for col in ['relative_humidity_2m:p', 'relative_humidity_10m:p', 'relative_humidity_1000hPa:p']:
                new_record = Humidity(
                    location_id=location_id,
                    date=dict['validdate'][i].date(),
                    time=dict['validdate'][i].time(),
                    value=dict[col][i],
                    level=col.split("_")[-1].split(":")[0],
                    unit=col.split(":")[-1]
                )
                session.add(new_record)


        if 'dew_point' in tables_to_update:
            for col in ['dew_point_2m:C', 'dew_point_10m:C', 'dew_point_1000hPa:C']:
                new_record = Dew(
                    location_id = location_id,
                    date=dict['validdate'][i].date(),
                    time=dict['validdate'][i].time(),
                    value=dict[col][i],
                    level=col.split("_")[-1].split(":")[0],
                    unit=col.split(":")[-1]
                )
                session.add(new_record)

        if 'pressure' in tables_to_update:
            new_record = Pressure(
                location_id = location_id,
                date=dict['validdate'][i].date(),
                time=dict['validdate'][i].time(),
                pressure_pa = dict['msl_pressure:Pa'][i],
            )
            session.add(new_record)

        if 'wind' in tables_to_update:
            new_record = Wind(
                location_id=location_id,
                date=dict['validdate'][i].date(),
                time=dict['validdate'][i].time(),
                wind_speed_2m_kmh=dict['wind_speed_2m:kmh'][i] if 'wind_speed_2m:kmh' in cols else None,
                wind_speed_5ft_kmh=dict['wind_speed_5ft:kmh'][i] if 'wind_speed_5ft:kmh' in cols else None,
                wind_speed_1000hpa_kmh = dict['wind_speed_1000hPa:kmh'][i] if 'wind_speed_1000hPa:kmh' in cols else None,
                wind_dir_2m_deg = dict['wind_dir_2m:d'][i] if 'wind_dir_2m:d' in cols else None,
                wind_dir_5ft_deg = dict['wind_dir_5ft:d'][i] if 'wind_dir_5ft:d' in cols else None,
                wind_dir_1000hpa_deg = dict['wind_dir_1000hPa:d'][i] if 'wind_dir_1000hPa:d' in cols else None
            )
            session.add(new_record)

        if 'cloud' in tables_to_update:
            for col in ['low_cloud_cover:octas', 'medium_cloud_cover:octas', 'high_cloud_cover:octas']:
                new_record = Cloud(
                    location_id = location_id,
                    date=dict['validdate'][i].date(),
                    time=dict['validdate'][i].time(),
                    value=dict[col][i],
                    level=col.split("_")[0],
                    unit=col.split(":")[-1]
                )
                session.add(new_record)


    session.commit()
    session.close()


