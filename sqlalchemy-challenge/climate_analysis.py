import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

currentDate = (session.query(Measurement.date)
                     .order_by(Measurement.date.desc())
                     .first())

currentDate = list(np.ravel(currentDate))[0]

currentDate = dt.datetime.strptime(currentDate, '%Y-%m-%d')

currentYear = int(dt.datetime.strftime(currentDate, '%Y'))
currentMonth = int(dt.datetime.strftime(currentDate, '%m'))
currentDay = int(dt.datetime.strftime(currentDate, '%d'))

last12months = dt.date(currentYear, currentMonth, currentDay) - dt.timedelta(days=365)
last12months = dt.datetime.strftime(last12months, '%Y-%m-%d')

@app.route("/")
def homepage():
    return (f"Available Routes:<br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/precipitaton <br/>"
            f"/api/v1.0/temperature <br/>"
            f"-------------------------------------------------<br/>"
            f"Date Search Routes:<br/>"
			f"-------------------------------------------------<br/>"
			f"/api/v1.0/datesearch/2017-01-01 <br/>"
            f"/api/v1.0/datesearch/2016-01-01/2017-01-01 <br/>"
            )


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                      .filter(Measurement.date > last12months)
                      .order_by(Measurement.date)
                      .all())
    
    precipData = []
    for result in results:
        precipDict = {result.date: result.prcp, "Station": result.station}
        precipData.append(precipDict)

    return jsonify(precipData)



@app.route("/api/v1.0/temperature")
def temperature():

    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
                      .filter(Measurement.date > last12months)
                      .order_by(Measurement.date)
                      .all())

    tempData = []
    for result in results:
        tempDict = {result.date: result.tobs, "Station": result.station}
        tempData.append(tempDict)

    return jsonify(tempData)



@app.route('/api/v1.0/datesearch/<startDate>')
def start(startDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= startDate)
                       .group_by(Measurement.date)
                       .all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)


@app.route('/api/v1.0/datesearch/<startDate>/<endDate>')
def startEnd(startDate, endDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= startDate)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) <= endDate)
                       .group_by(Measurement.date)
                       .all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)



if __name__ == "__main__":
    app.run(debug=True)