from flask import Flask, render_template, jsonify, redirect, url_for
import requests
import mysql.connector
from time import localtime, strftime, sleep
import threading
import json

app = Flask(__name__)

# Database connection - replace with your database credentials
conn = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="xxxxxxxxxxx",  
    database="weather_data" 
)
cursor = conn.cursor()

collecting_data = False

def current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def get_weather_data():
    response = requests.get("https://api.open-meteo.com/v1/forecast",
                            params={
                                "latitude": 49.33,
                                "longitude": 19.55,
                                "current": ["temperature_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m"]
                            })
    return response.json()

def store_weather_data():
    output = get_weather_data()
    temperature = output["current"]["temperature_2m"]
    wind_speed = output["current"]["wind_speed_10m"]
    surface_pressure = output["current"]["surface_pressure"]
    relative_humidity= output["current"]["relative_humidity_2m"]

    current_time_str = current_time()
    cursor.execute("INSERT INTO temperature_log (log_time, temperature, relative_humidity, surface_pressure, wind_speed) VALUES (%s, %s, %s, %s, %s)", 
                   (current_time_str, temperature, relative_humidity, surface_pressure, wind_speed))
    conn.commit()

def get_all_records():
    cursor.execute("SELECT * FROM temperature_log ORDER BY id DESC")
    return cursor.fetchall()

def auto_collect_data():
    global collecting_data
    
    while collecting_data:
        store_weather_data()
        sleep(5)  # Wait for 5 seconds before collecting data again

def export_to_json():
    cursor.execute("SELECT * FROM temperature_log")
    rows = cursor.fetchall()
    
    # Defining keys for JSON structure
    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "log_time": row[1].strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": row[2],
            "relative_humidity": row[3],
            "surface_pressure": row[4],
            "wind_speed": row[5]
        })

    # Export to a JSON file
    with open("weather_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("Data has been exported to weather_data.json")
    


@app.route('/')
def index():
    records = get_all_records()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add_record():
    store_weather_data()
    return redirect(url_for('index'))

@app.route('/start_auto_collect', methods=['POST'])
def start_auto_collect():
    global collecting_data
    if not collecting_data:
        collecting_data = True
        thread = threading.Thread(target=auto_collect_data)
        thread.start()
    return redirect(url_for('index'))

@app.route('/stop_auto_collect', methods=['POST'])
def stop_auto_collect():
    global collecting_data
    collecting_data = False
    return redirect(url_for('index'))

@app.route('/export_to_json', methods=['POST'])
def export_to_json_route():
    export_to_json()
    return redirect(url_for('index'))

@app.route('/data')
def get_data():
    records = get_all_records()
    return jsonify(records)


if __name__ == '__main__':
    app.run(debug=True)
