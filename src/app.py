import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


## Setup DB
engine = create_engine("sqlite:///../resources/hawaii.sqlite")


## Refelct existing DB and reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


## Activate Flask and Define Routes
app = Flask(__name__)

@app.route('/')
def root():
    return (
        f"Possible Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


###############################
## Station API Route
@app.route('/api/v1.0/precipitation')
def precipitation():

    """Precipitation Data for the most Recent Year"""
    session = Session(engine)

    ## Query to return the date and precipitation
    prcp_date_query = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    ## Convert query to dictionary
    prcp_date_list = []

    for date, prcp in prcp_date_query:
        prcp_date_dict = {}
        prcp_date_dict[date] = prcp
        prcp_date_list.append(prcp_date_dict)

    ## JSONIFY the dictionary
    return jsonify(prcp_date_list)


###############################
## Station API Route
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    station_query = session.query(Station.station,Station.name).all()

    ## Convert query to dictionary
    station_list = {}

    for station, name in station_query:
        station_list[station] = name

    ## JSONIFY the dictionary
    return jsonify (station_list)


###############################
## Station API Route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    station_query = session.query(Station.station,Station.name).all()

    ## Convert query to dictionary
    station_list = {}

    for station, name in station_query:
        station_list[station] = name

    ## JSONIFY the dictionary
    return jsonify (station_list)


###############################
## Station API Route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    station_query = session.query(Station.station,Station.name).all()

    ## Convert query to dictionary
    station_list = {}

    for station, name in station_query:
        station_list[station] = name

    ## JSONIFY the dictionary
    return jsonify (station_list)


if __name__ == '__main__':
    app.run(debug=True)
