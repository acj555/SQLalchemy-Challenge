# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

# Import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# ----------------------------------------
# Database Setup
# ----------------------------------------

# Create engine to connect to SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# ----------------------------------------
# Flask App Setup
# ----------------------------------------

app = Flask(__name__)

# ----------------------------------------
# Flask Routes
# ----------------------------------------

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"<h2>Welcome to the Hawaii Climate API!</h2>"
        f"<h3>Available Routes:</h3>"
        f"<ul>"
        f"<li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> - Last 12 months of precipitation data</li>"
        f"<li><a href='/api/v1.0/stations'>/api/v1.0/stations</a> - List of all stations</li>"
        f"<li><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> - Last 12 months of temperature observations for the most active station</li>"
        f"<li>/api/v1.0/&lt;start&gt; - Min, Avg, and Max temperature from start date</li>"
        f"<li>/api/v1.0/&lt;start&gt;/&lt;end&gt; - Min, Avg, and Max temperature for a date range</li>"
        f"</ul>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""

    # Create session (link) from Python to DB
    session = Session(engine)

    # Calculate the date one year ago from the most recent date
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in results}

    # Return JSON representation
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of all station IDs."""
    
    # Create session
    session = Session(engine)

    # Query all station IDs
    results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    # Return JSON list of station names
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the most active station (USC00519281)."""

    # Create session
    session = Session(engine)

    # Calculate date one year ago from last data point
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query last 12 months of temperature observations for most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    tobs_list = [{date: temp} for date, temp in results]

    # Return JSON list of temperature observations
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    """Return JSON with min, avg, and max temperature for a given start or start-end range."""

    # Create session
    session = Session(engine)

    # Select the min, avg, and max temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # If only start date is provided, get stats for all dates >= start date
    if end is None:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        # If both start and end date provided, get stats for that date range
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    # Close the session
    session.close()

    # Convert results into a dictionary
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": round(results[0][1], 2),
        "TMAX": results[0][2]
    }

    # Return JSON response
    return jsonify(temp_stats)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
