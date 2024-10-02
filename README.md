***For beginners friendly version please check out my simplified Python code: https://github.com/emax-77/OpenMeteo-to-MySQL-PythonOnlyVersion***
***A 5-second delay between each request in auto-collect mode is too small to get the relevant data, so I recommend using a delay of at least 30 seconds or more.***

# Python code for Flask that collects data from the Open-Meteo API, stores it in a MySQL database and exports it to a JSON file.

## Data for my GPS coordinates, you can change the coordinates in the script to get the weather data for your location.

# Required packages:
- Flask
- requests
- mysql.connector

## Setup the MySQL database:
- download MySQL database from https://dev.mysql.com/downloads/mysql/
- install and run MySQL console (MySQL Command Line Client)
- create a MySQL database "weather_data"
    - CREATE DATABASE weather_data;
- use the weather_data database:
    - USE weather_data;
- create a table for the weather data:
    - CREATE TABLE temperature_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_time DATETIME NOT NULL,
    temperature FLOAT NOT NULL,
    relative_humidity FLOAT NOT NULL,
    surface_pressure FLOAT NOT NULL,   
    wind_speed FLOAT NOT NULL  );
- change the database credentials in the script to match your MySQL database credentials

### Run the script:
- install the required packages using a pip
- clone the repository
- run the script :)

***For more info about free Open-Meteo API please visit https://open-meteo.com***


