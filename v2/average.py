import mysql.connector
from datetime import datetime, timedelta, timezone
from time import sleep
import sys
import os

#add path to sensors_fields.py and sensors_name.py
#because not in the same directory
sensors_data_path = os.environ.get('SENSORS_DATA_PATH')
if sensors_data_path is None:
    print("SENSORS_DATA_PATH environnement variable was not set")
    exit()
sys.path.insert(0, sensors_data_path)

from sensors_data import sensors
from sensors_features import sensor_areas, sensor_rooms

def get_area_id(area_name,mydb):
    #find the corresponding id to the sensor_name in the database
    #and check if the sensor is of the correct type
    mycursor = mydb.cursor()
    sql = "SELECT id FROM sensors_area \
            WHERE sensors_area.name = %s"
    val = (area_name,)
    
    try :
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None

    area_id = mycursor.fetchone()

    if area_id is None:
        print("The area name does not exist in the database")
        return None

    return area_id[0]
      
def get_room_id(room_name,mydb):
    #find the corresponding id to the sensor_name in the database
    #and check if the sensor is of the correct type
    mycursor = mydb.cursor()
    sql = "SELECT id FROM sensors_room \
            WHERE sensors_room.name = %s"
    val = (room_name,)
    
    try :
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None

    room_id = mycursor.fetchone()

    if room_id is None:
        print("The room name does not exist in the database")
        return None

    return room_id[0]


def WIA_avg_add_to_database(
        area_id, room_id, date_begin, date_end, temperature, humidity, light, motion, soundAvg, soundPeak, mydb):

    mycursor = mydb.cursor()
    sql = "INSERT INTO WIA_avg \
            (area_id, room_id, date_begin, date_end, temperature, humidity, light, motion, soundPeak, soundAvg) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (area_id, room_id, date_begin, date_end, temperature, humidity, light, motion, soundPeak, soundAvg) 
    
    try:
        mycursor.execute(sql, val)
        print("1 record inserted.")
        mydb.commit()
    except mysql.connector.Error as err:
        if(err.errno == 1062):
            print("Duplicate entry")
        else:
            print(err)
            return


def WIA_area_avg(area_name, date_begin, date_end, mydb):

    area_id = get_area_id(area_name, mydb)
    if area_id is None:
        print("The area name does not exist in the database")
        return None
    
    mycursor = mydb.cursor()
    if(area_name == "ALL_DCU"):
        sql = "SELECT avg(temperature), avg(humidity), avg(light), avg(motion), avg(soundPeak), avg(soundAvg) \
            FROM WIA_sensor INNER JOIN sensor ON sensor.id = WIA_sensor.sensor_id \
            WHERE time_recorded >= %s AND time_recorded <= %s"
        val = (date_begin, date_end)
    else:
        sql = "SELECT avg(temperature), avg(humidity), avg(light), avg(motion), avg(soundPeak), avg(soundAvg) \
            FROM WIA_sensor INNER JOIN sensor ON sensor.id = WIA_sensor.sensor_id \
            WHERE sensor.area = %s AND time_recorded >= %s AND time_recorded <= %s"
        val = (area_id, date_begin, date_end)

    mycursor.execute(sql, val)
    area_values = mycursor.fetchone()

    print("Temperature: " + str(area_values[0]) + "  Humidity: " + str(area_values[1]) + "  Light: " 
            + str(area_values[2]) + "  Motion: " + str(area_values[3]) + "  Sound Peak: " 
            + str(area_values[4]) + "  Sound Avg: " + str(area_values[5]))
    WIA_avg_add_to_database(area_id, None, date_begin, date_end, area_values[0], area_values[1],
                               area_values[2], area_values[3], area_values[4], area_values[5], mydb)

def WIA_room_avg(room_name, date_begin, date_end, mydb):

    room_id = get_room_id(room_name, mydb)
    if room_id is None:
        print("The room name does not exist in the database")
        return None

    mycursor = mydb.cursor()
    sql = "SELECT avg(temperature), avg(humidity), avg(light), avg(motion), avg(soundPeak), avg(soundAvg) \
           FROM WIA_sensor INNER JOIN sensor ON sensor.id = WIA_sensor.sensor_id \
           WHERE sensor.room = %s AND time_recorded >= %s AND time_recorded <= %s"
    val = (room_id, date_begin, date_end)

    mycursor.execute(sql, val)
    room_values = mycursor.fetchone()

    print("Temperature: " + str(room_values[0]) + "  Humidity: " + str(room_values[1]) + "  Light: " 
            + str(room_values[2]) + "  Motion: " + str(room_values[3]) + "  Sound Peak: " 
            + str(room_values[4]) + "  Sound Avg: " + str(room_values[5]))
    WIA_avg_add_to_database(None, room_id, date_begin, date_end, room_values[0], room_values[1],
                               room_values[2], room_values[3], room_values[4], room_values[5], mydb)


def HiData_avg_add_to_database(area_id, date_begin, date_end, occupancy, light, noise, mydb):
    
        mycursor = mydb.cursor()
        sql = "INSERT INTO HiData_avg \
                (area_id, date_begin, date_end, occupancy, light, noise) \
                values (%s, %s, %s, %s, %s, %s)"
        val = (area_id, date_begin, date_end, occupancy, light, noise) 
        
        try:
            mycursor.execute(sql, val)
            print("1 record inserted.")
            mydb.commit()
        except mysql.connector.Error as err:
            if(err.errno == 1062):
                print("Duplicate entry")
            else:
                print(err)
                return

def HiData_avg(area_name, date_begin, date_end, mydb):
    
        area_id = get_area_id(area_name, mydb)
        if area_id is None:
            print("The area name does not exist in the database")
            return None
        
        mycursor = mydb.cursor()
        sql = "SELECT avg(occupancy), avg(light), avg(noise) \
            FROM HiData_sensor INNER JOIN sensor ON sensor.id = HiData_sensor.sensor_id \
            WHERE sensor.area = %s AND time_recorded >= %s AND time_recorded <= %s"
        val = (area_id, date_begin, date_end)
    
        mycursor.execute(sql, val)
        area_values = mycursor.fetchone()
        print(area_values)
    
        print("Occupancy: " + str(area_values[0]) + "  Light: " + str(area_values[1]) 
            + "  Noise: " + str(area_values[2]))
        HiData_avg_add_to_database(area_id, date_begin, date_end, area_values[0], area_values[1],
                                area_values[2], mydb)

if __name__ == "__main__":

    #get the mysql host
    mysql_host = os.environ.get('MYSQL_HOST')
    if mysql_host is None:
        print("MYSQL_HOST environnement variable was not set")
        exit()

    #get the mysql user
    mysql_user = os.environ.get('MYSQL_USER')
    if mysql_user is None:
        print("MYSQL_USER environnement variable was not set")
        exit()

    #get the mysql password
    mysql_pwd = os.environ.get('MYSQL_PWD')
    if mysql_pwd is None:
        print("MYSQL_PWD environnement variable was not set")
        exit()
    
    #database connection
    mydb = mysql.connector.connect(
    host = mysql_host,
    user = mysql_user,
    password = mysql_pwd,
    database = "sensors"
    )

    while True:

        interval = 15
        #1 hour interval to get the data avg per area
        today = datetime.now()
        wia_avg_date_begin = today - timedelta(minutes=interval)
        WIA_AVG_DATE_BEGIN = wia_avg_date_begin.strftime('%Y-%m-%d %H:%M:%S')
        WIA_AVG_DATE_END = today.strftime('%Y-%m-%d %H:%M:%S') 

        print(WIA_AVG_DATE_BEGIN)
        print(WIA_AVG_DATE_END)

        for area in sensor_areas:
            print(area)
            WIA_area_avg(area, WIA_AVG_DATE_BEGIN, WIA_AVG_DATE_END, mydb)
            #HiData_avg(area, HIDATA_AVG_DATE_BEGIN, HIDATA_AVG_DATE_END, mydb)
        for room in sensor_rooms:
            print(room)
            WIA_room_avg(room, WIA_AVG_DATE_BEGIN, WIA_AVG_DATE_END, mydb)

        #get avg every 15 minutes
        sleep(60 * interval)

