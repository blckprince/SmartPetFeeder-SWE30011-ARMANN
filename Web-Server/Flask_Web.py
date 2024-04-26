from flask import Flask, render_template, jsonify
import mysql.connector
import serial
import time

app = Flask(__name__)



# Connect to Arduino serial port
ser = serial.Serial('/dev/ttyUSB0', 9600)

@app.route('/')
def index():
    # Connect to MySQL database
    mydb = mysql.connector.connect(host="localhost",user="pi",password="1234",database="assgntwo_db")

    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM food_level WHERE id = 1")
    food_level_data = cursor.fetchone()
    
    cursor.execute("SELECT * FROM bowl_level WHERE id = 1")
    bowl_level_data = cursor.fetchone()
    
    cursor.close()
    mydb.close()
    return render_template('index.html', food_level=food_level_data, bowl_level=bowl_level_data)


@app.route('/food_level')
def get_food_level():
    
    mydb = mysql.connector.connect(host="localhost",user="pi",password="1234",database="assgntwo_db")

    cursor = mydb.cursor()
    
    # Fetch data from the database
    cursor.execute("SELECT * FROM food_level WHERE id = 1")
    food_level_data = cursor.fetchone()
    
    print("Food Level:", food_level_data[1])
    print("Last Update Time:", food_level_data[2])
    cursor.close()
    mydb.close()
    
    return jsonify({'level': food_level_data[1], 'time': food_level_data[2]})
    return render_template('index.html', food_level=food_level_data)


@app.route('/bowl_level')
def get_bowl_level():
    
    mydb = mysql.connector.connect(host="localhost",user="pi",password="1234",database="assgntwo_db")

    cursor = mydb.cursor()
    
    # Fetch data from the database
    cursor.execute("SELECT * FROM bowl_level WHERE id = 1")
    bowl_level_data = cursor.fetchone()
    
    print("bowl Level:", bowl_level_data[1])
    print("Last Update Time:", bowl_level_data[2])
    cursor.close()
    mydb.close()
    
    return jsonify({'level': bowl_level_data[1], 'time': bowl_level_data[2]})
    return render_template('index.html', bowl_level=bowl_level_data)
    


@app.route('/dispense')
def dispense_food():
    # Send '1' to Arduino to dispense food
    ser.write(b'1')

    # Insert a new row into the food_dispense table
    sql = "INSERT INTO food_dispense (value, date_time) VALUES (%s, %s)"
    val = (1, time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(sql, val)
    mydb.commit()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

