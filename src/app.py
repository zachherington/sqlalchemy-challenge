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
Station = Base.classes.Station


## Activate Flask and Define Routes
app = Flask(__name__)

@app.route('/')
def root():
    return (
        f"Possible Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures: /api/v1.0/tobs<br/>"
        f"Temp Data from start date: /api/v1.0/temp/<start><br/>"
        f"Temp Data from start to end date: /api/v1.0/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation

if __name__ == '__main__':
    app.run()
