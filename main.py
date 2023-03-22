from data_storage.setup_db import create_all_tables
from fastapi import FastAPI, status, HTTPException
import utils.utils as utils
from data_storage.read_db import read_db, get_captions, get_coords_by_caption

# Create all tables in the database
create_all_tables()

# Fast API Handling
app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"status": 'ok', "instructions": "Hi. You can use the /measures/ to continue"}

@app.get("/measures/")
def read_measures(lat: float, lon: float, caption:str=None, startdate:int=None, ndays:int=1, measure:str=None):
    if lat == None or lon == None:
        raise HTTPException(status_code=422,  detail="You have to especify a latitude and a longitude")

    if measure == None:
        raise HTTPException(status_code=422,  detail="You have to especify a measure")

    if measure not in utils.valid_measures:
        raise HTTPException(status_code=422, detail=f"The measure is not valid. You should use one of the following: {', '.join(utils.valid_measures)}")

    db_data = read_db({"lat": lat, "lon": lon, 'caption': caption, 'date': utils.int_to_date(startdate),
                       'final_date': utils.get_final_date(startdate, ndays), 'n_days': ndays,
                       'measures': [measure]})

    if db_data is None:
        raise HTTPException(status_code=404, detail=f"Data not found")

    return db_data, 200

# Get data by caption
@app.get("/measures/bycaption/")
def measures_by_caption(caption:str=None, startdate:int=None, ndays:int=1, measure:str=None):
    coords = get_coords_by_caption(caption)

    if coords == None:
        raise HTTPException(status_code=422, detail="The caption is not valid")

    if measure == None:
         raise HTTPException(status_code=422,  detail="You have to especify a measure")

    if measure not in utils.valid_measures:
         raise HTTPException(status_code=422, detail=f"The measure is not valid. You should use one of the following: {', '.join(utils.valid_measures)}")

    db_data = read_db({"lat": coords['lat'], "lon": coords['lon'], 'date': utils.int_to_date(startdate),
                        'final_date': utils.get_final_date(startdate, ndays), 'n_days': ndays,
                        'measures': [measure]})

    if db_data is None:
         raise HTTPException(status_code=404, detail=f"Data not found")

    return db_data, 200



@app.get("/list/measures/", status_code=status.HTTP_200_OK)
def list_measures():
    return {"status": 'ok', "instructions": f"You can use the following measures to get your data: {', '.join(utils.valid_measures)}"}

# List all available captions
@app.get("/list/captions/", status_code=status.HTTP_200_OK)
def list_captions():

    if len(get_captions()) == 0:
        raise HTTPException(status_code=404, detail="No captions found")
    return {"status": "ok", "captions_available": ', '.join(get_captions())}