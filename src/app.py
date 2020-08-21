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
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start<start>/end<end><br/>"
    )


###############################
## Precipitation API Route
@app.route('/api/v1.0/precipitation')
def precipitation():

    ## Query to return the date and precipitation
    session = Session(engine)
    prcp_date_query = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    ## Convert query to dictionary
    prcp_date_list = [{"Date":"Precipitation (inches)"}]

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

    ## Query to return the list of stations
    session = Session(engine)
    station_query = session.query(Station.station,Station.name).all()

    ## Convert query to dictionary
    station_list = {"Station ID":"Station Name"}

    for station, name in station_query:
        station_list[station] = name

    ## JSONIFY the dictionary
    return jsonify (station_list)


###############################
## Observed Temperature API Route
@app.route('/api/v1.0/tobs')
def tobs():

    ## Query to find the most recent date and the date for one year prior
    session = Session(engine)
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    prev_year_date = dt.datetime.strptime(most_recent_date[0],'%Y-%m-%d')-dt.timedelta(days=365)
    prev_year_date_formatted = prev_year_date.strftime('%Y-%m-%d')

    ## Query to get the 12 months of data
    temp_query = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= prev_year_date_formatted).\
                    order_by(Measurement.date).all()

    ## Convert query to dictionary
    tobs_date_list = [{"Date":"Temperature (F)"}]

    for date, tobs in temp_query:
        tobs_date_dict = {}
        tobs_date_dict[date] = tobs
        tobs_date_list.append(tobs_date_dict)

    ## JSONIFY the dictionary
    return jsonify (tobs_date_list)


###############################
## Start Date Temp Data API Route
@app.route('/api/v1.0/start<start>')
def temp_data_start(start):

    ## Query to return the list of stations
    session = Session(engine)
    
    temp_start_list = []
    
    temp_start_query = session.query(func.min(Measurement.tobs),\
                                    func.max(Measurement.tobs),\
                                    func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()

    ## Convert query to dictionary
    for min, max, avg in temp_start_query:
        temp_start_dict = {}
        temp_start_dict["Min Temp"] = min
        temp_start_dict["Max Temp"] = max
        temp_start_dict["Avg Temp"] = avg
        temp_start_list.append(temp_start_dict)

    ## JSONIFY the dictionary
    return jsonify (temp_start_list)


# ###############################
# ## Station API Route
# @app.route('/api/v1.0/start<start>/end<end>')
# def temp_data_start(start,end):

#     ## Query to return the list of stations
#     session = Session(engine)
#     station_query = session.query(Station.station,Station.name).all()

#     ## Convert query to dictionary
#     station_list = {}

#     for station, name in station_query:
#         station_list[station] = name

#     ## JSONIFY the dictionary
#     return jsonify (station_list)

if __name__ == '__main__':
    app.run(debug=True)
