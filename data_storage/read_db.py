from sqlalchemy import Table, MetaData, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data_storage.db import get_engine
from data_storage.setup_db import Location, Temperature, Humidity, Dew, Pressure, Wind, Cloud
from data_collection.call_weather import call_met
from data_storage.update_db import add_location

# Function called by @app.get("/measures/"). It first try to find the measure in DB, filtered by start/end date.
# If nothing is found, it calls Meteomatics API to populate the DB
def read_db(obj):

    # First check if the location ID exists. If not, add it to DB
    location_id = check_location_exists(obj)['location_id']
    # Return the data from the measure based on the parameters
    table_content = return_single_table(obj, location_id)

    # If there is no data in DB, it call Meteomatics (call_met)
    if table_content == None:
        call_met(obj['lat'], obj['lon'], obj['n_days'], obj['measures'])
        table_content = return_single_table(obj, location_id)

    return table_content

def check_location_exists(obj):
    location_exists = None
    metadata = MetaData()
    engine = get_engine()
    location_table = Table('location', metadata, autoload_with=engine)

    # Check if the location (lon/lat) exists in DB
    select_statement = location_table.select().where(
        and_(
            location_table.c.lon == obj['lon'], location_table.c.lat == obj['lat']
        )
    )

    with engine.connect() as conn:
        result = conn.execute(select_statement).fetchall()
        if len(result) > 0:
            location_id = result[0][0]
            location_exists = True
        else:
            # If location does not exists, add it and after run the Select again
            add_location(obj['lat'], obj['lon'], obj['caption'])
            location_exists = False

    if location_exists == False:
        result = conn.execute(select_statement).fetchall()
        location_id = result[0][0]

    return {'location_id': location_id}


def return_single_table(obj, location_id):
    measure_name = obj['measures'][0] # Get the measure name
    response_package = {"title": f"{measure_name} data", "data": {}}
    row_counter = 0

    engine = get_engine()
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Dict to connect measure names and table classes
    table_dictionary = {
        "temperature": Temperature,
        "humidity": Humidity,
        "dew_point": Dew,
        "pressure": Pressure,
        "wind": Wind,
        "cloud_cover": Cloud
    }

    # Query to get entries from DB. It works with Location table and join it with the specific measure table,
    # filtered by location_id and by initial/final date
    measure_table = session.query(Location, table_dictionary[measure_name]) \
        .join(table_dictionary[measure_name]) \
        .filter(Location.location_id == location_id) \
        .filter(table_dictionary[measure_name].date >= obj['date']) \
        .filter(table_dictionary[measure_name].date <=obj ['final_date'])\
        .all()

    # If no date is found, return None to call Meteomatics
    if len(measure_table) == 0:
        return None

    # Loop to add all entries from all columns in a dictionary and return it
    for location, measure in measure_table:
        location_dict = {k: v for k, v in location.__dict__.items() if not k.startswith('_')}
        measure_dict = {k: v for k, v in measure.__dict__.items() if not k.startswith('_')}

        response_package["data"][str(row_counter)] = {
            "location": location_dict,
            f"{measure_name}": measure_dict,
        }
        row_counter = row_counter + 1

    return response_package

# Function to list all available captions
def get_captions():
    caption_list = []
    metadata = MetaData()
    engine = get_engine()
    location_table = Table('location', metadata, autoload_with=engine)

    # Check if the location (lon/lat) exists in DB
    select_statement = location_table.select()

    with engine.connect() as conn:
        result = conn.execute(select_statement).fetchall()

        for loc in result:
            if loc.caption is not None:
                caption_list.append(loc.caption)

    return caption_list

# Function get the place coordinates by caption, and return the data
def get_coords_by_caption(caption):
    coords = {}
    metadata = MetaData()
    engine = get_engine()
    location_table = Table('location', metadata, autoload_with=engine)

    # Check if the location (lon/lat) exists in DB
    select_statement = location_table.select().where(location_table.c.caption == caption)

    with engine.connect() as conn:
        result = conn.execute(select_statement).fetchall()
        if len(result) == 0:
            return None
        else:
            coords['lat'] = result[0].lat
            coords['lon'] = result[0].lon

    return coords