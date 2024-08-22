from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
import mysql.connector
from time import localtime, strftime, sleep
import threading

app = Flask(__name__)

# Database connection - replace with your database credentials
conn = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="19Peter77+",  
    database="weather_data" 
)
cursor = conn.cursor()

collecting_data = False

def current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def get_weather_data():
    response = requests.get("https://api.open-meteo.com/v1/forecast",
                            params={
                                "latitude": 49.322740,
                                "longitude": 19.551755,
                                "current_weather": True
                            })
    return response.json()

def store_weather_data():
    output = get_weather_data()
    temperature = output["current_weather"]["temperature"]
    current_time_str = current_time()
    cursor.execute("INSERT INTO temperature_log (log_time, temperature) VALUES (%s, %s)", 
                   (current_time_str, temperature))
    conn.commit()

def get_all_records():
    cursor.execute("SELECT * FROM temperature_log ORDER BY id DESC")
    return cursor.fetchall()

def auto_collect_data():
    global collecting_data
    start_time = localtime()
    
    while collecting_data:
        store_weather_data()
        sleep(5)  # Wait for 5 seconds before collecting data again
        
        # Stop after one hour
        #elapsed_time = time.mktime(localtime()) - time.mktime(start_time)
        #if elapsed_time >= 3600:
        #    collecting_data = False

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

@app.route('/data')
def get_data():
    records = get_all_records()
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)
