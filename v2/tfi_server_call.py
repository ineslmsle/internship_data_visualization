import requests
import json
import mysql.connector
import os
from time import sleep
import haversine
import sys


STOP_ID=0
STOP_CODE=1
STOP_NAME=2
STOP_DESC=3
STOP_LAT=4
STOP_LON=5
ZONE_ID=6
STOP_URL=7
LOCATION_TYPE=8
PARENT_STATION=9

x_dcu_center = 53.3850
y_dcu_center = -6.2578

# usage
n = len(sys.argv)
if n <= 2:
    print("Usage: python3 tfi_server_call.py <diameter1> <diameter2> ...")
    sys.exit()

diameters = [int(sys.argv[i]) for i in range(1,n)]


def get_stops_in_circle(circle_radius_meters):

    with open('stops.txt', 'r') as f: 
        # Skip the header
        next(f) 
        count = 0
        stops = []
        # Read and process the remaining lines 
        for line in f: 
            if "\"" in line:
                continue

            line = line.split(",")
            x_stop = float(line[STOP_LAT])
            y_stop = float(line[STOP_LON])

            distance=haversine.haversine((x_stop, y_stop), 
                                        (x_dcu_center, y_dcu_center), 
                                        unit=haversine.Unit.METERS)
            
            if distance < circle_radius_meters:
                count += 1
                stops.append(line)
            
    return stops
 
def TFI_server_call(stop,mydb):
    #call format to the API
    url = 'http://localhost:7341/api/v1/arrivals?stop=' + str(stop)
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        j_response = json.loads(response.text)

        json_formatted_str = json.dumps(j_response, indent=2)

        #print(json_formatted_str)

        for arrival in j_response[str(stop)]['arrivals']:
            print(arrival['scheduled_arrival'])

            mycursor = mydb.cursor()
            sql = "INSERT INTO TFI_bus_stop \
                  (bus_stop_id,route, headsign, scheduled_arrival) \
                   VALUES (%s, %s, %s, %s)"
            val = (stop,arrival['route'],arrival['headsign'],arrival['scheduled_arrival'])
            
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


    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


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

    mycursor = mydb.cursor()
    sql = "DELETE FROM TFI_bus_stop"
    val = ()
    
    try:
        mycursor.execute(sql, val)
        print("table cleared")
        mydb.commit()
    except mysql.connector.Error as err:
        print(err)


    for diameter in diameters:
        print("diameter: ", diameter)
        stops=get_stops_in_circle(diameter)
        bus_stop_ids = [stop[STOP_CODE] for stop in stops]
        for stop in bus_stop_ids:
            print("stop: ", stop)
            TFI_server_call(stop,mydb)

        print(" ")

    sleep(30)
