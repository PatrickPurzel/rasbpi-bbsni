import paho.mqtt.client as mqtt
import time
import sched
import threading
from gpiozero import CPUTemperature
import mysql.connector
from mysql.connector import Error

# Define MQTT Broker
c_host    = "mosquitto"
c_port    = 1883
c_timeout = 60

# Define MySQL Server
sql_host = "sysman-db"
sql_user = "user"
sql_pw   = "password"
sql_port = 3306
sql_db   = "test_database"

#
s_five = sched.scheduler(time.time, time.sleep)
s_fivesec = sched.scheduler(time.time, time.sleep)


# Create Table if non existent 
def create_table(table_name):
    insert_txt = "CREATE TABLE IF NOT EXISTS " + str(table_name) + " (id INT NOT NULL AUTO_INCREMENT, time datetime, temprature FLOAT, PRIMARY KEY (id))"

    cursor.execute(insert_txt)

    connection.commit()

# Insert current CPU Temprature and time into table
def table_insert(table_name):
    # Gets current time in hours and minutes
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Gets current CPU temprature
    current_temp = CPUTemperature()
    current_temp = current_temp.temperature

    # Construction of the SQL string to write data to the Database table
    insert_txt = "INSERT INTO " + str(table_name) + " (temprature, time) VALUES (%s, %s)"
    insert_val = (current_temp, current_time)

    cursor.execute(insert_txt, insert_val)

    connection.commit()

#Check if connection to Database is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Send Data via MQTT at specified topic
def pub_send(topic, payload, qos):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish(topic, payload=payload, qos=qos, retain=False)
    #print(f"send {payload} to {topic}")

# Connecting to MySQL Database
def create_connection(host_name, user_name, user_password, host_port, db_name):
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=host_port,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn

def thread_db():
    s_five.enter(5, 1, run_db, (s_five,))
    s_five.run()


    

def run_db(sc):
    # Insert Value ot Table
    table_insert("test_table1")
    sc.enter(5, 1, run_db, (sc,))

def run_mqtt(sc):
    # send a message to the raspberry/topic
    cpu = CPUTemperature()
    #print(cpu.temperature)
    pub_send('raspberry/topic', cpu.temperature, 0)
    time.sleep(1)
    #client.loop_forever()
    sc.enter(5, 1, run_mqtt, (sc,))


def init():
    global cursor
    global connection
    global client

    # Connecting to Database and init process
    connection = create_connection(sql_host, sql_user, sql_pw, sql_port, sql_db)
    cursor = connection.cursor()
    create_table("test_table1")
    

    # Init MQTT Connection
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(c_host, c_port, c_timeout)

def main():
    init()

    x = threading.Thread(target=thread_db)
    x.start()

    s_fivesec.enter(5, 1, run_mqtt, (s_fivesec,))
    s_fivesec.run()




if __name__ == '__main__':
    main()