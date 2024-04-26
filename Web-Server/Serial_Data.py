import mysql.connector
import serial
import time

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="pi",
    password="1234",
    database="assgntwo_db"
)

cursor = mydb.cursor()

# Read serial data from Arduino for food level and bowl level
def read_sensor_data():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            if line in ['full', 'low', 'dark', 'light']:
                if line in ['full', 'low']:
                    # Update the food level in the database
                    sql = "UPDATE food_level SET level = %s, time = %s WHERE id = 1"
                    val = (line, time.strftime('%Y-%m-%d %H:%M:%S'))
                    print("Food level:", line, ". Database updated.")
                else:
                    # Update the bowl level in the database
                    sql = "UPDATE bowl_level SET food = %s, time = %s WHERE id = 1"
                    val = ('Have Food' if line == 'dark' else 'No Food', time.strftime('%Y-%m-%d %H:%M:%S'))
                    print("Bowl level:", line, ". Database updated.")

                cursor.execute(sql, val)
                mydb.commit()

try:
    read_sensor_data()
except KeyboardInterrupt:
    cursor.close()
    mydb.close()
