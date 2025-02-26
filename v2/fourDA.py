import mysql.connector
import requests
import json
from datetime import datetime
import sys

#add path to sensors_fields.py and sensors_name.py
#because not in the same directory
sys.path.insert(0, '/home/ines/internship_2ndyear')

from sensors_data import sensors

WIA_4DA_SENSORS = 40
WIA_4DA_BEGIN_VALUE = 6654
WIA_END_VALUE = WIA_4DA_BEGIN_VALUE + 6*WIA_4DA_SENSORS

BBB_4DA_BEGIN_VALUE_READ = 7188
BBB_4DA_BEGIN_VALUE_PERC = 7198
BBB_4DA_BEGIN_VALUE = BBB_4DA_BEGIN_VALUE_READ
BBB_4DA_END_VALUE = 7204

CIVIC_4DA_Z0_BEGIN_PEDESTRIAN = 6935
CIVIC_4DA_Z0_BEGIN_BIKE = 6940

CIVIC_4DA_Z1_BEGIN_PEDESTRIAN = 6945
CIVIC_4DA_Z1_BEGIN_BIKE = 6950

CIVIC_4DA_Z2_BEGIN_LONG_TRUCK = 6955
CIVIC_4DA_Z2_BEGIN_MOTORBIKE = 6960
CIVIC_4DA_Z2_BEGIN_SHORT_TRUCK = 6965
CIVIC_4DA_Z2_BEGIN_CAR = 6970
CIVIC_4DA_Z2_BEGIN_BIKE = 6975
CIVIC_4DA_Z2_BEGIN_UNDEFINED = 6980

CIVIC_4DA_Z3_BEGIN_LONG_TRUCK = 6985
CIVIC_4DA_Z3_BEGIN_MOTORBIKE = 6990
CIVIC_4DA_Z3_BEGIN_SHORT_TRUCK = 6995
CIVIC_4DA_Z3_BEGIN_CAR = 7000   
CIVIC_4DA_Z3_BEGIN_BIKE = 7005
CIVIC_4DA_Z3_BEGIN_UNDEFINED = 7010

CIVIC_4DA_Z4_BEGIN_LONG_TRUCK = 7015
CIVIC_4DA_Z4_BEGIN_MOTORBIKE = 7020
CIVIC_4DA_Z4_BEGIN_SHORT_TRUCK = 7025
CIVIC_4DA_Z4_BEGIN_CAR = 7030
#CIVIC_4DA_Z4_BEGIN_BIKE = 7035
CIVIC_4DA_Z4_BEGIN_UNDEFINED = 7035

CIVIC_4DA_Z5_BEGIN_LONG_TRUCK = 7040
CIVIC_4DA_Z5_BEGIN_MOTORBIKE = 7045
CIVIC_4DA_Z5_BEGIN_SHORT_TRUCK = 7050
CIVIC_4DA_Z5_BEGIN_CAR = 7055
CIVIC_4DA_Z5_BEGIN_BIKE = 7060
CIVIC_4DA_Z5_BEGIN_UNDEFINED = 7065

CIVIC_4DA_Z6_BEGIN_PEDESTRIAN = 7070
CIVIC_4DA_Z6_BEGIN_BIKE = 7075

CIVIC_4DA_Z7_BEGIN_PEDESTRIAN = 7080
CIVIC_4DA_Z7_BEGIN_BIKE = 7085

CIVIC_4DA_Z8_BEGIN_PEDESTRIAN = 7090
CIVIC_4DA_Z8_BEGIN_BIKE = 7095

CIVIC_4DA_Z9_BEGIN_PEDESTRIAN = 7100
CIVIC_4DA_Z9_BEGIN_BIKE = 7105

CIVIC_4DA_BEGIN_VALUE = 6935
CIVIC_4DA_END_VALUE = 7104


def fourDA_get_sensor_id(sensor_name, sensor_type, mydb):
    if(sensor_type != '4DA_WIA' and 
       sensor_type != '4DA_BBB' and 
       sensor_type != '4DA_CIVIC'):
        print("The sensor type does not exist")
        return None
    
    mycursor = mydb.cursor()
    sql = "select sensor.id from sensor \
        inner join sensors_types on sensor.type=sensors_types.id \
        where sensor.name = %s and sensors_types.name = \'" + sensor_type + "_TYPE\';"
    val = (str(sensor_name),)

    try :
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None

    sensor_id = mycursor.fetchone()

    if sensor_id is None:
        print("The sensor name does not exist in the database or is not a " + sensor_type +" sensor")
        return None

    return sensor_id[0]


def fourDA_WIA_get_value_number(value_type, sensor_name):
    #check if value type argument is correct
    #value from 1 to 6 given by 4DA
    value_type_number = 0
    if value_type == "light":
        value_type_number = 0
    elif value_type == "temperature":
        value_type_number = 1
    elif value_type == "humidity":
        value_type_number = 2
    elif value_type == "motion":
        value_type_number = 3
    elif value_type == "soundPeak":
        value_type_number = 4
    elif value_type == "soundAvg":
        value_type_number = 5
    else:
        print("The value type \"" + str(value_type) + "\" does not exist")
        return None

    value_number = value_type_number + WIA_4DA_BEGIN_VALUE + (int(sensor_name)-1)*6

    if(value_number > WIA_END_VALUE or value_number < WIA_4DA_BEGIN_VALUE):
        print("Error in the value type given or sensor id")
        return
    
    return value_number

def fourDA_BBB_get_value_number(value_type, sensor_name):
    #check if value type argument is correct
    #value from 1 to 2 given by 4DA
    value = 0
    if value_type == "reading":
        value = BBB_4DA_BEGIN_VALUE_READ
    elif value_type == "percentage":
        value = BBB_4DA_BEGIN_VALUE_PERC
    else:
        print("The value type \"" + value_type + "\" does not exist")
        return None

    if(sensor_name== "DCU - Londis - General Waste & Pizza Belly - TRASH" ):
        value = value + 0
    elif(sensor_name== "DCU - Londis - General Waste & Pizza Belly - BOTTLE_CANS" ):
        value = value + 1
    elif(sensor_name== "DCU - Londis - General Waste & Pizza Belly - COMPOSTABLES" ):
        value = value + 2
    elif(sensor_name== "DCU - Londis - General Waste & Pizza Belly - PAPER"):
        value = value + 3
    elif(sensor_name== "DCU - New Paved Picnic Plaza Next To Albert College - BOTTLE_CANS" ):
        value = value + 4
    elif(sensor_name== "DCU - New Paved Picnic Plaza Next To Albert College - TRASH" ):
        value = value + 5
    elif(sensor_name== "DCU - New Paved Picnic Plaza Next To Albert College - COMPOSTABLES" ):
        value = value + 6
    else:
        print(" \" "+ sensor_name + " \" is not a BBB sensor")
        return None

    if(value > BBB_4DA_END_VALUE or value < BBB_4DA_BEGIN_VALUE):
        print("Error in the value type given or sensor id")
        return None
    
    return value

def fourDA_CIVIC_get_value_number(value_type, sensor_name):
    value = 0
    if(sensor_name== "Zone 0 - DCU Main Entrance - PEDESTRIAN" ):
        value = CIVIC_4DA_Z0_BEGIN_PEDESTRIAN
    elif(sensor_name== "Zone 0 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z0_BEGIN_BIKE
    elif(sensor_name== "Zone 1 - DCU Main Entrance - PEDESTRIAN" ):
        value = CIVIC_4DA_Z1_BEGIN_PEDESTRIAN
    elif(sensor_name== "Zone 1 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z1_BEGIN_BIKE
    elif(sensor_name== "Zone 2 - DCU Main Entrance - LONG TRUCK" ):
        value = CIVIC_4DA_Z2_BEGIN_LONG_TRUCK
    elif(sensor_name== "Zone 2 - DCU Main Entrance - MOTORBIKE" ):
        value = CIVIC_4DA_Z2_BEGIN_MOTORBIKE
    elif(sensor_name== "Zone 2 - DCU Main Entrance - SHORT TRUCK" ):
        value = CIVIC_4DA_Z2_BEGIN_SHORT_TRUCK
    elif(sensor_name== "Zone 2 - DCU Main Entrance - CAR" ):
        value = CIVIC_4DA_Z2_BEGIN_CAR
    elif(sensor_name== "Zone 2 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z2_BEGIN_BIKE
    elif(sensor_name== "Zone 2 - DCU Main Entrance - UNDEFINED" ):
        value = CIVIC_4DA_Z2_BEGIN_UNDEFINED
    elif(sensor_name== "Zone 3 - DCU Main Entrance - LONG TRUCK" ):
        value = CIVIC_4DA_Z3_BEGIN_LONG_TRUCK
    elif(sensor_name== "Zone 3 - DCU Main Entrance - MOTORBIKE" ):
        value = CIVIC_4DA_Z3_BEGIN_MOTORBIKE
    elif(sensor_name== "Zone 3 - DCU Main Entrance - SHORT TRUCK" ):
        value = CIVIC_4DA_Z3_BEGIN_SHORT_TRUCK
    elif(sensor_name== "Zone 3 - DCU Main Entrance - CAR" ):
        value = CIVIC_4DA_Z3_BEGIN_CAR
    elif(sensor_name== "Zone 3 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z3_BEGIN_BIKE
    elif(sensor_name== "Zone 3 - DCU Main Entrance - UNDEFINED" ):
        value = CIVIC_4DA_Z3_BEGIN_UNDEFINED
    elif(sensor_name== "Zone 4 - DCU Main Entrance - LONG TRUCK" ):
        value = CIVIC_4DA_Z3_BEGIN_LONG_TRUCK
    elif(sensor_name== "Zone 4 - DCU Main Entrance - MOTORBIKE" ):
        value = CIVIC_4DA_Z4_BEGIN_MOTORBIKE
    elif(sensor_name== "Zone 4 - DCU Main Entrance - SHORT TRUCK" ):
        value = CIVIC_4DA_Z4_BEGIN_SHORT_TRUCK
    elif(sensor_name== "Zone 4 - DCU Main Entrance - CAR" ):
        value = CIVIC_4DA_Z4_BEGIN_CAR
    elif(sensor_name== "Zone 4 - DCU Main Entrance - UNDEFINED" ):
        value = CIVIC_4DA_Z4_BEGIN_UNDEFINED
    elif(sensor_name== "Zone 5 - DCU Main Entrance - LONG TRUCK" ):
        value = CIVIC_4DA_Z5_BEGIN_LONG_TRUCK
    elif(sensor_name== "Zone 5 - DCU Main Entrance - MOTORBIKE" ):
        value = CIVIC_4DA_Z5_BEGIN_MOTORBIKE
    elif(sensor_name== "Zone 5 - DCU Main Entrance - SHORT TRUCK" ):
        value = CIVIC_4DA_Z5_BEGIN_SHORT_TRUCK
    elif(sensor_name== "Zone 5 - DCU Main Entrance - CAR" ):
        value = CIVIC_4DA_Z5_BEGIN_CAR
    elif(sensor_name== "Zone 5 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z5_BEGIN_BIKE
    elif(sensor_name== "Zone 5 - DCU Main Entrance - UNDEFINED" ):
        value = CIVIC_4DA_Z5_BEGIN_UNDEFINED
    elif(sensor_name== "Zone 6 - DCU Main Entrance - PEDESTRIAN" ):
        value = CIVIC_4DA_Z6_BEGIN_PEDESTRIAN
    elif(sensor_name== "Zone 6 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z6_BEGIN_BIKE
    elif(sensor_name== "Zone 7 - DCU Main Entrance - PEDESTRIAN" ):
        value = CIVIC_4DA_Z7_BEGIN_PEDESTRIAN
    elif(sensor_name== "Zone 7 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z7_BEGIN_BIKE
    elif(sensor_name== "Zone 8 - DCU Main Entrance - PEDESTRIAN" ):
        value = CIVIC_4DA_Z8_BEGIN_PEDESTRIAN
    elif(sensor_name== "Zone 8 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z8_BEGIN_BIKE
    elif(sensor_name== "Zone 9 - DCU Main Entrance - PEDESTRIAN" ):
        value = CIVIC_4DA_Z9_BEGIN_PEDESTRIAN
    elif(sensor_name== "Zone 9 - DCU Main Entrance - BIKE" ):
        value = CIVIC_4DA_Z9_BEGIN_BIKE
    else:
        print(" \" "+ sensor_name + " \" is not a CIVIC sensor")
        return None

    #check if value type argument is correct
    #value from 1 to 5 given by 4DA
    if value_type == "speed":
        value += 0
    elif value_type == "headway":
        value += 1
    elif value_type == "occupancy":
        value += 2
    elif value_type == "gap":
        value += 3
    elif value_type == "volume":
        value += 4
    else:
        print("The value type \"" + value_type + "\" does not exist")
        return None

    if(value > CIVIC_4DA_END_VALUE or value < CIVIC_4DA_BEGIN_VALUE):
        print("Error in the value type given or sensor id")
        return None
    
    return value


def fourDA_add_to_database(value_type, value, date, sensor_id, sensor_type, mydb):
    if(sensor_type != '4DA_WIA' and 
       sensor_type != '4DA_BBB' and 
       sensor_type != '4DA_CIVIC'):
        print("The sensor type does not exist")
        return None
    
    mycursor = mydb.cursor()
    sql = "insert into " + sensor_type + "_sensor (type, value, time_recorded, sensor_id) \
           select " + sensor_type + "_types.id, %s, %s, %s from " + sensor_type + "_types \
           where " + sensor_type + "_types.name = %s;"

    val = (value, date, sensor_id, value_type)
    
    try:
        mycursor.execute(sql, val)
        print("1 record inserted.")
        mydb.commit()
    except mysql.connector.Error as err:
        if(err.errno == 1062):
            print("Duplicate entry")
        else:
            print(err)


def fourDA_API_call(sensor_id, value_type, value_number, date_begin, date_end, limit, sensor_type, mydb):
    if(sensor_type != '4DA_WIA' and 
       sensor_type != '4DA_BBB' and 
       sensor_type != '4DA_CIVIC'):
        print("The sensor type does not exist")
        return None

    #call format to the API
    url = 'https://4da-dcu-svc.bentley.com/resources/Datas?Parent=' + str(value_number) + '&StartDate=' + date_begin + '%2000%3A00%3A00&EndDate=' + date_end + '%2000%3A00%3A00&Top=' + str(limit) + '&='
    headers = {
        'Authorization': 'Basic amFpbWVib2FuZXJqZXMuZmVybmFuZGV6cm9ibGVyb0BkY3UuaWU6QmVudGx5ZGN1cGFzczEyIw==',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        j_response = json.loads(response.text)
        if j_response['data'] == []:
            print("No data")
            return

        #saving the file
        with open('/home/ines/internship_2ndyear/data/4DA_' + str(value_number) + '.json', 'w') as f:
            f.write(response.text)
        f.close()

        for data in j_response['data']:
            date = datetime.strptime(data['timetag'], '%Y-%m-%d %H:%M:%S')
            fourDA_add_to_database(value_type, data['value'], date, sensor_id, sensor_type, mydb)


    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def fourDA_API_calls( date_begin, date_end, WIA_limit, BBB_limit, CIVIC_limit, mydb):
    print("4DA API calls")
    ################# 4DA WIA #################
    fourDA_WIA_types = ["light", "temperature", "humidity", "motion", "soundPeak", "soundAvg"]

    for sensor in sensors:
        if sensor['type'] == '4DA_WIA_TYPE':
            sensor_name = sensor['name']
            print(sensor_name)
            sensor_id = fourDA_get_sensor_id(sensor_name, '4DA_WIA', mydb)
            if sensor_id is None:
                continue

            for value_type in fourDA_WIA_types:
                print(value_type)
                value_number = fourDA_WIA_get_value_number(value_type, sensor_name)
                if value_number is None:
                    continue
                fourDA_API_call(sensor_id, value_type, value_number, date_begin, date_end, WIA_limit,'4DA_WIA', mydb)

    ################# 4DA BBB #################
    fourDA_BBB_types = ["reading","percentage"]

    for sensor in sensors:
        if sensor['type'] == '4DA_BBB_TYPE':
            sensor_name = sensor['name']
            print(sensor_name)
            sensor_id = fourDA_get_sensor_id(sensor_name, '4DA_BBB', mydb)
            if sensor_id is None:
                continue

            for value_type in fourDA_BBB_types:
                print(value_type)
                value_number = fourDA_BBB_get_value_number(value_type, sensor_name)
                if value_number is None:
                    continue
                fourDA_API_call(sensor_id, value_type, value_number, date_begin, date_end, BBB_limit, '4DA_BBB', mydb)

    ################# 4DA CIVIC #################
    fourDA_CIVIC_types = ["speed", "headway", "occupancy", "gap", "volume"]

    for sensor in sensors:
        if sensor['type'] == '4DA_CIVIC_TYPE':
            sensor_name = sensor['name']
            print(sensor_name)
            sensor_id = fourDA_get_sensor_id(sensor_name, '4DA_CIVIC', mydb)
            if sensor_id is None:
                continue

            for value_type in fourDA_CIVIC_types:
                print(value_type)
                value_number = fourDA_CIVIC_get_value_number(value_type, sensor_name)
                if value_number is None:
                    continue
                fourDA_API_call(sensor_id, value_type, value_number, date_begin, date_end, CIVIC_limit, '4DA_CIVIC', mydb)
