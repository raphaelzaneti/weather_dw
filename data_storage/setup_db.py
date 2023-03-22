from sqlalchemy import ForeignKey,  Column, Integer, Float, DateTime, String, inspect, Time, Date
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import declarative_base
from data_storage.db import get_engine

# This module create the database from zero

engine = get_engine()
inspector = inspect(engine)
Base = declarative_base()

# Landing table, where any response from Meteomatics will be stored
class Landing(Base):
    __tablename__ = 'landing'
    request_id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    requested_at = Column(DateTime)
    date_value = Column(DateTime)
    parameter = Column(String(50))
    value = Column(Float)
    unit = Column(String(5))


# To avoid repetitions, we store the lat/long in a locations table, using location_id as foreign key for measures tables
class Location(Base):
    __tablename__ = 'location'
    location_id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    caption = Column(String(20), unique=True)

# All table measures are build in long format, except for wind and pressure, which are wide.
class Temperature(Base):
    __tablename__ = 'temperature'
    temperature_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    time = Column(Time)
    value = Column(Float)
    level = Column(String)
    unit = Column(String)
    '''
    temp_2m_celsius = Column(Float)
    temp_10m_celsius = Column(Float)
    temp_1000hpa_celsius = Column(Float)
    '''
    location = relationship(Location)


class Humidity(Base):
    __tablename__ = 'humidity'
    humidity_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    time = Column(Time)
    value = Column(Float)
    level = Column(String)
    unit = Column(String)
    location = relationship(Location)


class Dew(Base):
    __tablename__ = 'dew_point'
    dew_point_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    time = Column(Time)
    value = Column(Float)
    level = Column(String)
    unit = Column(String)
    '''
    dew_point_2m_celsius = Column(Float)
    dew_point_10m_celsius = Column(Float)
    dew_point_1000hpa_celsius = Column(Float)
    '''
    location = relationship(Location)


class Pressure(Base):
    __tablename__ = 'pressure'
    pressure_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    time = Column(Time)
    pressure_pa = Column(Float)
    location = relationship(Location)


class Wind(Base):
    __tablename__ = 'wind'
    wind_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    time = Column(Time)
    wind_speed_2m_kmh = Column(Float)
    wind_speed_5ft_kmh = Column(Float)
    wind_speed_1000hpa_kmh = Column(Float)
    wind_dir_2m_deg = Column(Integer)
    wind_dir_5ft_deg = Column(Integer)
    wind_dir_1000hpa_deg = Column(Integer)
    location = relationship(Location)


class Cloud(Base):
    __tablename__ = 'cloud_cover'
    cloud_cover_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    time = Column(Time)
    value = Column(Float)
    level = Column(String)
    unit = Column(String)
    '''
    low_cloud_cover_octas = Column(Float)
    medium_cloud_cover_octas = Column(Float)
    high_cloud_cover_octas = Column(Float)
    '''
    location = relationship(Location)

def create_all_tables():

    Base.metadata.create_all(engine)