import mysql.connector
import requests
import csv
from datetime import datetime
import sys

#add path to sensors_fields.py and sensors_name.py
#because not in the same directory
sys.path.insert(0, '/home/ines/internship_2ndyear')

from sensors_data import sensors

def HiData_get_sensor_id(sensor_name,mydb):
    #find the corresponding id to the sensor_name in the database
    #and check if the sensor is of the correct type
    mycursor = mydb.cursor()
    sql = "SELECT sensor.id FROM sensor \
            INNER JOIN sensors_types ON sensor.type=sensors_types.id \
            WHERE sensor.name = %s AND sensors_types.name = 'HIDATA_TYPE'"
    val = (sensor_name,)

    try :
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None

    sensor_id = mycursor.fetchone()

    if sensor_id is None:
        print("The sensor name does not exist in the database or is not a HiData sensor")
        return None

    return sensor_id[0]

def HiData_add_to_database(occupancy, light, noise, date, sensor_id, mydb):

    mycursor = mydb.cursor()
    sql = "insert into HiData_sensor (occupancy, light, noise, time_recorded, sensor_id) values (%s, %s, %s, %s, %s)"
    val = (occupancy, light, noise,  date, sensor_id)
    
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
        
def HiData_API_call(sensor_name, sensor_id, limit, mydb):

    #call format to the API
    url = 'http://20.61.174.172/APIV1/data?filename=' + sensor_name + '.csv'

    try:
        response = requests.get(url)
        response.raise_for_status()

        #saving the file
        with open('/home/ines/internship_2ndyear/data/HiData' + sensor_name + '.csv', 'w') as f:
            f.write(response.text)
        f.close()

        #parsing csv file and removing unwanted characters (header)
        #to improve !
        csv_file = response.text
        csv_file = csv_file.split('[[')  
        csv_file = csv_file[1].split(']]')      
        csv_file = csv_file[0].split('], [')
        csv_file = csv.reader(csv_file)

        for row in csv_file:

            if(csv_file.line_num > limit): #to not do all the file
                return

            #remove unwanted characters
            row[0] = row[0].replace('\\\"', '')
            row[1] = row[1].replace('\\\"', '')
            row[2] = row[2].replace('\\\"', '')
            row[3] = row[3].replace('\\\"', '')

            date = datetime.strptime(row[0], '%d-%m-%Y %H:%M:%S')
            HiData_add_to_database(row[1], row[2], row[3], date, sensor_id, mydb)    

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def HiData_API_calls(limit, mydb):
    print("HiData API calls")
    for sensor in sensors:
        if(sensor['type'] == 'HIDATA_TYPE'):
            sensor_name = sensor['name']
            print(sensor_name)
            sensor_id = HiData_get_sensor_id(sensor_name, mydb)
            if sensor_id is None:
                continue
            HiData_API_call(sensor_name, sensor_id, limit, mydb)

