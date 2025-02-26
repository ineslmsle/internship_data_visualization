import mysql.connector
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
from sensors_features import fourDA_WIA_fields, fourDA_CIVIC_fields, fourDA_BBB_fields
from sensors_features import sensor_types, sensor_areas, sensor_rooms, CIVIC_classes
from sensors_features import firebase_types


def insert_sensor(sensor,mydb):
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into sensor \
            (type,name,serial_number, number, area, room, longitude, latitude, altitude) \
            SELECT sensors_types.id, %s, %s, %s, sensors_area.id, sensors_room.id, %s, %s, %s \
            FROM sensors_types, sensors_area, sensors_room \
            WHERE sensors_types.name = %s \
            AND sensors_area.name = %s \
            AND sensors_room.name = %s ;"
        
        val = (sensor['name'], sensor['serial_number'], sensor['number'],
            sensor['longitude'], sensor['latitude'], sensor['altitude'], 
            sensor['type'], sensor['area'], sensor['room'],)
        
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(sensor['name'] + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None

def insert_fourDA_fields(mydb):
    #4DA WIA fields
    for field in fourDA_WIA_fields:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into 4DA_WIA_types (name) values (%s)"
        val = (field,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(field + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None
            
    #4DA BBB fields
    for field in fourDA_BBB_fields:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into 4DA_BBB_types (name) values (%s)"
        val = (field,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(field + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None
            
    #4DA CIVIC fields
    for field in fourDA_CIVIC_fields:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into 4DA_CIVIC_types (name) values (%s)"
        val = (field,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(field + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None

def insert_sensor_types(mydb):
    for sensor_type in sensor_types:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into sensors_types (name) values (%s)"
        val = (sensor_type,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(sensor_type + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None
        
def insert_sensor_areas(mydb):
    for sensor_area in sensor_areas:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into sensors_area (name) values (%s)"
        val = (sensor_area,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(sensor_area + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None
        
def insert_sensor_rooms(mydb):
    for sensor_room in sensor_rooms:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into sensors_room (name) values (%s)"
        val = (sensor_room,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(sensor_room + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None

def insert_CIVIC_classes(mydb):
    for CIVIC_class in CIVIC_classes:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into CIVIC_class (name) values (%s)"
        val = (CIVIC_class,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(CIVIC_class + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None

def insert_firebase_types(mydb): 
    for firebase_type in firebase_types:
        mycursor = mydb.cursor(buffered=True)
        sql = "INSERT into Firebase_types (name) values (%s)"
        val = (firebase_type,)
        try :
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount == 0):
                print(" 0 record inserted.")
            else:
                print(firebase_type + " inserted into the database.")

        except mysql.connector.Error as err:
            print(err)
            return None


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

    #insert sensor types into the database
    insert_sensor_types(mydb)
    #insert sensor areas into the database
    insert_sensor_areas(mydb)
    #insert sensor rooms into the database
    insert_sensor_rooms(mydb)
    #insert 4DA fields into the database
    insert_fourDA_fields(mydb)
    #insert CIVIC classes into the database
    insert_CIVIC_classes(mydb)
    #insert firebase types into the database
    insert_firebase_types(mydb)

    #insert all sensors into the database
    for sensor in sensors:
        insert_sensor(sensor,mydb)

    mydb.close()
