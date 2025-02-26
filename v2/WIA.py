import mysql.connector
import requests
import json
from datetime import datetime
import sys

#add path to sensors_fields.py and sensors_name.py
#because not in the same directory
sys.path.insert(0, '/home/ines/internship_2ndyear')

from sensors_data import sensors

def WIA_get_sensor_id(sensor_name,mydb):
    #find the corresponding id to the sensor_name in the database
    #and check if the sensor is of the correct type
    mycursor = mydb.cursor()
    sql = "select sensor.id from sensor \
            inner join sensors_types on sensor.type=sensors_types.id \
            where sensor.name = %s and sensors_types.name = 'WIA_TYPE'"
    val = (sensor_name,)
    
    try :
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None

    sensor_id = mycursor.fetchone()

    if sensor_id is None:
        print("The sensor name does not exist in the database or is not a WIA sensor")
        return None

    return sensor_id[0]

def WIA_add_to_database(temperature, humidity, light, motion, soundAvg, soundPeak, date, sensor_id, mydb):

    mycursor = mydb.cursor()
    sql = "insert into WIA_sensor \
            (temperature, humidity, light, motion, soundAvg, soundPeak, time_recorded, sensor_id) \
            values (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (temperature,humidity,light,motion,soundPeak,soundAvg, date, sensor_id)
    
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

def WIA_API_call(sensor_id, sensor_name, limit, mydb):
    #call format to the API
    url = 'https://api.wia.io/v1/events?device.id=' + sensor_name + '&processed=true&limit=' + str(limit)
    headers = {
        'Authorization': 'Bearer a_sk_XE739N4A2V0gWNbbRhzxCke1',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        j_response = json.loads(response.text)
        if(len(j_response['events']) == 0):
            print("No data to be inserted into the database")
            return

        #saving the file
        with open('/home/ines/internship_2ndyear/data/WIA_' + sensor_name + '.json', 'w') as f:
            f.write(response.text)
        f.close()

        #initialize timestamps values
        timestamp_current = j_response['events'][0]['timestamp']
        timestamp_previous = j_response['events'][0]['timestamp']

        #initialize field values
        temperature = 0.0
        humidity = 0.0
        light = 0.0
        motion = 0.0
        soundPeak = 0.0
        soundAvg = 0.0

        for event in j_response['events']:

            timestamp_current = event['timestamp']

            if(event['name'] == 'temperature'):
                temperature = event['data']
            elif(event['name'] == 'humidity'):
                humidity = event['data']
            elif(event['name'] == 'light'):
                light = event['data']
            elif(event['name'] == 'motion'):
                motion = event['data']
            elif(event['name'] == 'soundPeak'):
                soundPeak = event['data']
            elif(event['name'] == 'soundAvg'):
                soundAvg = event['data']

            if(timestamp_current != timestamp_previous):

                date = datetime.fromtimestamp(event['timestamp']/1000)
                WIA_add_to_database(temperature, humidity, light, motion, soundPeak, soundAvg, date, sensor_id, mydb)

                timestamp_previous = timestamp_current

                temperature = 0.0
                humidity = 0.0
                light = 0.0
                motion = 0.0
                soundPeak = 0.0
                soundAvg = 0.0

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

def WIA_API_calls(limit, mydb):
    print("WIA API calls")
    for sensor in sensors:
        if(sensor['type'] == 'WIA_TYPE'):
            sensor_name = sensor['name']
            sensor_id = WIA_get_sensor_id(sensor_name, mydb)
            if sensor_id is None:
                continue
            WIA_API_call(sensor_id, sensor_name, limit, mydb)

