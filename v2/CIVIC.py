import mysql.connector
import requests
import csv
from datetime import datetime
from datetime import timezone

def CIVIC_get_sensor_id(sensor_name,mydb):
    mycursor = mydb.cursor(buffered=True)
    sql = "select sensor.id from sensor \
        inner join sensors_types on sensor.type=sensors_types.id \
            where sensor.name = %s and sensors_types.name = 'CIVIC_TYPE'"
    val = (sensor_name,)

    try:
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None
    
    sensor_id = mycursor.fetchone()

    if sensor_id is None:
        print("The sensor name does not exist in the database or is not a CIVIC sensor")
        return None

    return sensor_id[0]

def CIVIC_add_to_database(date_begin, date_end, zone, asset,data_class,speed,headway,occupancy,gap,volume,sensor_id, mydb):

    mycursor = mydb.cursor(buffered=True)
    sql = "insert into CIVIC_sensor (date_begin, date_end, zone, asset,class,speed,headway,occupancy,gap,volume,sensor_id) select %s,%s,%s,%s,CIVIC_class.id,%s,%s,%s,%s,%s,%s from CIVIC_class where CIVIC_class.name = %s;"
    val = (date_begin, date_end, zone, asset, speed, headway, occupancy, gap, volume, sensor_id, data_class)

    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print("1 record inserted.")
    except mysql.connector.Error as err:
        if(err.errno == 1062):
            print("Duplicate entry")
        else:
            print(err)
            return

def CIVIC_API_call(asset, date_begin, date_end, limit, mydb):
    #call format to the API
    url = 'https://radar-api.ipsum365.com/tcounts/csv/' + str(asset) +'?start=' + date_begin + '&end=' + date_end
    headers = {
        'x-api-key': 'AEgSlpd2bn3pzVtfoTiV916bi9U6r9Yt34O1l8zp',
        'Content-Type': 'application/csv'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        #saving the file
        with open('/home/ines/internship_2ndyear/data/CIVIC_' + str(asset) + '.csv', 'w') as f:
            f.write(response.text)
        f.close()

        csv_file = response.text
        csv_file = csv_file.split('\n')  
        csv_file = csv.reader(csv_file)

        row_count = 0
        for row in csv_file:
            if(row_count!= 0 and row != [] and row_count<=limit):
                #sensor name
                entrance = ""
                if(asset == 258930):
                    entrance = " - DCU Main Entrance - "
                elif(asset == 258943):
                    entrance = " - DCU Entrance - Ballymun Road - "
                elif(asset == 258934):
                    entrance = " - DCU Pedestrian Entrance - Collins Avenue - "
                else:
                    print("The asset does not exist")
                    return
                
                sensor_name = row[2] + entrance + row[4]
                sensor_id = CIVIC_get_sensor_id(sensor_name,mydb)
                print(sensor_name)

                #date conversion for mysql format
                date_begin_row = datetime.fromisoformat(row[0][:-1]).astimezone(timezone.utc)
                date_begin_row.strftime('%Y-%m-%d %H:%M:%S')

                date_end_row = datetime.fromisoformat(row[1][:-1]).astimezone(timezone.utc)
                date_end_row.strftime('%Y-%m-%d %H:%M:%S')

                CIVIC_add_to_database(date_begin_row, date_end_row, row[2][-1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], sensor_id, mydb)

            row_count += 1

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

def CIVIC_API_calls(date_begin, date_end, limit, mydb):
    print("CIVIC API calls")
    CIVIC_assets=[258930, 258943]
    for asset in CIVIC_assets:
        CIVIC_API_call(asset, date_begin, date_end, limit, mydb)
        