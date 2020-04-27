import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

measurement_first_row = session.query(Measurement).first()
measurement_first_row.__dict__

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all passengers
    results = session.query(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers

    results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station == "USC00519281").all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """change the format of date input"""
    dic = {"/":"-"," ":"-"}

    def replace_all(start, dic):
        for i, j in dic.iteritems():
            new_start = start.replace(i, j)
        return new_start
    
    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    query_temp = session.query(*sel).\
        filter(Measurement.date >= new_start).all()

    return jsonify(query_temp)

@app.route("/api/v1.0/<start>/<end>")

def start_date(start,end):
    """change the format of date input"""
    dic = {"/":"-"," ":"-"}

    def replace_all(start, dic):
        for i, j in dic.iteritems():
            new_start = start.replace(i, j)
        return new_start
    
     def replace_all(end, dic):
        for i, j in dic.iteritems():
            new_end = start.replace(i, j)
        return new_end

    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]

    query_temp = session.query(*sel).\
        filter(Measurement.date >= new_start).\
        filter(Measurement.date < new_end).all()

    return jsonify(query_temp)
