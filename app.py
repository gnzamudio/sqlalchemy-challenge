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
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("Welcome to the Hawaii Climate page</br>"
            "Below are the available routes:</br>"
            "/api/v1.0/precipitation</br>"
            "/api/v1.0/stations</br>"
            "/api/v1.0/tobs</br>"
            "/api/v1.0/start. date as (YYYY-MM-DD)</br>"
            "/api/v1.0/start/end. date as (YYYY-MM-DD)</br>")

@app.route("/api/v1.0/precipitation")
@app.route("/api/v1.0/stations")
@app.route("/api/v1.0/tobs")
@app.route("/api/v1.0/<startdate>")
@app.route("/api/v1.0/<startdate>/<enddate>")

if __name__ == "__main__":
    app.run(debug=True)    