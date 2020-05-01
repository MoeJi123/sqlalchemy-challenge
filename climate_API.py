import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value"""
    
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    session.close()

    return jsonify( prcp)


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    session.close()

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data"""

    results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station == "USC00519281").all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_date(start):

    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    query_temp = session.query(*sel).\
        filter(Measurement.date >= start).all()

    return jsonify(query_temp)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):

    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    query_temp = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date < end).all()

    return jsonify(query_temp)

if __name__ == '__main__':
    app.run(debug=True)