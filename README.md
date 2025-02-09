# SQLalchemy-Challenge
Overview
This project analyzes climate data from Hawaii using SQLAlchemy, Pandas, Matplotlib, and Flask. The assignment consists of two parts:

Jupyter Notebook Data Analysis – Queries climate data, performs precipitation & station analysis, and visualizes temperature trends.
Flask API Development – Creates an API to serve climate data dynamically via JSON responses.


Part 1: Climate Data Analysis (Jupyter Notebook)
The notebook (climate_starter_deliverable.ipynb) performs the following:

Connects to an SQLite database using SQLAlchemy.
Retrieves precipitation data for the last 12 months and plots the results.
Analyzes weather stations, including identifying the most active station.
Calculates min, max, and average temperatures for the most active station.
Plots a histogram of temperature observations.

Part 2: Flask API Development
The Flask app (app.py) creates an API with the following endpoints:

📍 Homepage (/) – Displays available API routes.
📍 Precipitation (/api/v1.0/precipitation) – Returns the last 12 months of precipitation data.
📍 Stations (/api/v1.0/stations) – Returns a list of all weather stations.
📍 Temperature Observations (/api/v1.0/tobs) – Returns temperature data for the most active station.
📍 Temperature Stats (/api/v1.0/<start> and /api/v1.0/<start>/<end>) – Returns min, avg, and max temperatures for a given date range.
