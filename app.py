import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Start the session
    session = Session(engine)

    #Record the results
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close() 
    
    #Record entries into database
    precipitation_list = []
    
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['Date'] = date
        precipitation_dict['Precipitation'] = prcp
        precipitation_list.append(precipitation_dict) 

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    #Start the session
    session = Session(engine)

    #Record the results
    results = session.query(Measurement.station).all()

    session.close() 
    
    #Record entries into database
    station_list = []
    
    for station in results:
        station_dict = {}
        station_dict['Station'] = station
        station_list.append(station_dict) 

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #Start the session
    session = Session(engine)

    #Record the results
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.station == 'USC00519281').all()

    session.close() 
    
    #Record entries into database
    most_active_list = []
    
    for date, tobs in results:
        most_active_dict = {}
        most_active_dict['Date'] = date
        most_active_dict['Temp.'] = tobs
        most_active_list.append(most_active_dict) 

    return jsonify(most_active_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end = None):

    canonicalized = start.replace(" ", "").lower()
    
    session = Session(engine)
    if not end:
        
        result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
        
    else:  
        result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    temp_average = list(np.ravel(result))

    session.close() 


    return jsonify(temp_average)

if __name__ == '__main__':
    app.run(debug=True)