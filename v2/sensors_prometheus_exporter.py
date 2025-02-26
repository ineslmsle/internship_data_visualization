from prometheus_client import start_http_server, Gauge
import time
import requests
import json
from datetime import datetime, timedelta
from datetime import timezone

# Create a metric temperature
WIA_temperature = Gauge('WIA_temperature', 'The temperature of the room',['sensor_name','area', 'room'])
WIA_light = Gauge('WIA_light', 'The light of the room',['sensor_name','area','room'])
WIA_humidity = Gauge('WIA_humidity', 'The humidity of the room',['sensor_name','area','room'])
WIA_motion = Gauge('WIA_motion', 'The motion of the room',['sensor_name','area','room'])
WIA_soundAvg = Gauge('WIA_soundAvg', 'The average sound of the room',['sensor_name','area','room'])
WIA_soundPeak = Gauge('WIA_soundPeak', 'The peak sound of the room',['sensor_name','area','room'])

civic_speed = Gauge('CIVIC_speed', 'The speed of the room',['sensor_name','area','room'])
civic_headway = Gauge('CIVIC_headway', 'The headway of the room',['sensor_name','area','room'])
civic_occupancy = Gauge('CIVIC_occupancy', 'The occupancy of the room',['sensor_name','area','room'])
civic_gap = Gauge('CIVIC_gap', 'The gap of the room',['sensor_name','area','room'])
civic_volume = Gauge('CIVIC_volume', 'The volume of the room',['sensor_name','area','room'])

def wia_api_call(sensor_name, area, room):
    #call format to the API
    print("Calling WIA API")
    url = 'https://api.wia.io/v1/events?device.id='+sensor_name+'&processed=true&limit=6'
    headers = {
        'Authorization': 'Bearer a_sk_XE739N4A2V0gWNbbRhzxCke1',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        j_response = json.loads(response.text)

        for event in j_response['events']:
            if(event['name'] == 'temperature'):
                WIA_temperature.labels(sensor_name=sensor_name, area=area, room=room).set(event['data'])
            elif(event['name'] == 'light'):
                WIA_light.labels(sensor_name=sensor_name, area=area, room=room).set(event['data'])
            elif(event['name'] == 'humidity'):
                WIA_humidity.labels(sensor_name=sensor_name, area=area, room=room).set(event['data'])
            elif(event['name'] == 'motion'):
                WIA_motion.labels(sensor_name=sensor_name, area=area, room=room).set(event['data'])
            elif(event['name'] == 'soundAvg'):
                WIA_soundAvg.labels(sensor_name=sensor_name, area=area, room=room).set(event['data'])
            elif(event['name'] == 'soundPeak'):
                WIA_soundPeak.labels(sensor_name=sensor_name, area=area, room=room).set(event['data'])
            else:
                print("Unknown data") 


    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

def CIVIC_api_call(asset, area, room):
    #beginning and end date calculation
    #change timezone to UTC

    today = datetime.now().astimezone(timezone.utc)
    print(today)
    date_end = today.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(date_end)
    time_interval = timedelta(hours=2)
    date_begin = today - time_interval 
    date_begin = date_begin.strftime('%Y-%m-%dT%H:%M:%SZ')


    #call format to the API
    print("Calling CIVIC API")
    url = 'https://radar-api.ipsum365.com/tcounts/json/' + asset +'?start=' + date_begin + '&end=' + date_end
    print(url)
    headers = {
        'x-api-key': 'AEgSlpd2bn3pzVtfoTiV916bi9U6r9Yt34O1l8zp',
        'Content-Type': 'application/csv'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        j_response = json.loads(response.text)


        for event in j_response:
            sensor_name = event['ZONE'] + ' ' + event['ASSET'] + ' ' + event['CLASS']

            print(sensor_name)

            civic_speed.labels(sensor_name=sensor_name, area=area, room=room).set(event['SPEED'])
            civic_headway.labels(sensor_name=sensor_name, area=area, room=room).set(event['HEADWAY'])
            civic_occupancy.labels(sensor_name=sensor_name, area=area, room=room).set(event['OCCUPANCY'])
            civic_gap.labels(sensor_name=sensor_name, area=area, room=room).set(event['GAP'])
            civic_volume.labels(sensor_name=sensor_name, area=area, room=room).set(event['VOLUME'])



    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    print("Server started on port 8000")
    
    # Generate some requests.
    while True:
        #to do for all sensors
        wia_api_call("dev_OhjroeDo", "Business School", "Room 1")
        wia_api_call("dev_1f43VXgG", "Stokes Building", "Room 2")
        wia_api_call("dev_klkV9Q10", "Stokes Building", "Room 3")

        CIVIC_api_call("258930", "Business School", "Room 1")
        
        #sleep to avoid too many requests
        time.sleep(5) 
