from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import psycopg2

app = Flask(__name__)

load_dotenv()
# Pobieranie danych połączenia z Railway z zmiennych środowiskowych
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")  # Domyślny port PostgreSQL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Połączenie z bazą danych PostgreSQL
def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    return connection

@app.route('/data', methods=['POST'])
def insert_data():
    # Odbieranie danych z urządzenia ESP32
    data = request.get_json()

    device_id = data['device_id']
    lux = data['lux']
    temperature = data['temperature']
    humidity = data['humidity']
    pressure = data['pressure']

    # Połączenie z bazą danych
    conn = get_db_connection()
    cursor = conn.cursor()

    # Wstawianie danych do tabeli sensor_data
    cursor.execute("""
        INSERT INTO sensor_data (device_id, lux, temperature, humidity, pressure)
        VALUES (%s, %s, %s, %s, %s)
    """, (device_id, lux, temperature, humidity, pressure))

    conn.commit()  # Zatwierdzanie transakcji
    cursor.close()
    conn.close()  # Zamknięcie połączenia z bazą danych

    return jsonify({"message": "Data inserted successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)