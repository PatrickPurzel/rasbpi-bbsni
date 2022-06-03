import paho.mqtt.client as mqtt
import time
from gpiozero import CPUTemperature
import mysql.connector
from mysql.connector import Error

# Define MQTT Broker location
c_host=     "localhost"
c_port=     1883
c_timeout=  60

# Create Table if non existent 
def create_table(table_connection, table_name):
    cursor = table_connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test_table1 (data_id INT, temprature FLOAT, time INT)")

# Insert Value into given Table
def table_insert(table_connection, val_temp, val_time):
    cursor = table_connection.cursor()
    insert_txt = "INSERT INTO test_table1 (temprature, time) VALUES (%s, %s)"
    insert_val = (val_temp, val_time)
    cursor.execute(insert_txt, insert_val)
    connection.commit()

#C heck if connection to Database is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Send Data via MQTT at specified topic
def pub_send(topic, payload, qos):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish(topic, payload=payload, qos=qos, retain=False)
    print(f"send {payload} to {topic}")

# Connecting to MySQL Database
def create_connection(host_name, user_name, user_password, host_port, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=host_port,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

### MAIN ###

# Connecting to Database and init process
connection = create_connection("localhost", "user", "password", 33306, "test_database")
create_table(connection, "test_table1")

# Insert Value ot Table
table_insert(connection, 10, 800)

# Init MQTT Connection
client = mqtt.Client()
client.on_connect = on_connect
client.connect(c_host, c_port, c_timeout)

# send a message to the raspberry/topic
while(True):
    cpu = CPUTemperature()
    print(cpu.temperature)
    pub_send('raspberry/topic', cpu.temperature, 0)
    time.sleep(1)
    #client.loop_forever()