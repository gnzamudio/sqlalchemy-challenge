#dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#create engine and prepare to reflect

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create an app, pass __name__

app = Flask(__name__)

#Define what to do when a user hits the index route
#List all routes that are available.

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("Welcome to the Hawaii Climate page</br>"
            "Available routes:</br>"
            "/api/v1.0/precipitation</br>"
            "/api/v1.0/stations</br>"
            "/api/v1.0/tobs</br>"
            "/api/v1.0/start. date as (YYYY-MM-DD)</br>"
            "/api/v1.0/start/end. date as (YYYY-MM-DD)</br>")

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_q= session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    precip_data = []
    for date, prcp in prcp_q:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp  
        precip_data.append(precip_dict) 
    return jsonify(precip_data)

#stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_q = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()
    stations = []
    for station, name, lat, lng, ele in station_q:
        station_dict= {}
        station_dict['Station'] = station
        station_dict['Name'] = name
        station_dict['Latitude'] = lat
        station_dict['Longitude'] = lng
        station_dict['Elevation'] = ele
        stations.append(station_dict)

    return jsonify(stations)

#temperature observations of the most active station for the last year

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_st = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    mostactive = active_st[0][0]
    mostactive_q = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == mostactive).all() 
    session.close()
    most_active_tobs = []
    for date, tobs in mostactive_q:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Temp'] = tobs
        most_active_tobs.append(tobs_dict)
    return jsonify(most_active_tobs)


#When given the start date, calculate TEMP MIN, AVG, and MAX for all dates after the given date
@app.route("/api/v1.0/<startdate>")
def start_tobs(start):
    session = Session(engine)
    start_q = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    start_data = []
    for min, avg, max in start_q:
        start_dict = {}
        start_dict['Minimum Temp'] = min
        start_dict['Average Temp'] = avg
        start_dict['Maximum Temp'] = max
        start_data.append(start_dict)
    return jsonify(start_data)

## When given the start and the end date, calculate the Temp MIN, AVG, and MAX for dates between the start and end date
@app.route("/api/v1.0/<startdate>/<enddate>")
def end_tobs(start,end):
    session = Session(engine)
    end_q = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    end_data = []
    for min, avg, max in end_q:
        end_dict = {}
        end_dict['Minimum Temp'] = min
        end_dict['Average Temp'] = avg
        end_dict['Maximum Temp'] = max
        end_data.append(end_dict)
    return jsonify(end_data)

if __name__ == "__main__":
    app.run(debug=True)    