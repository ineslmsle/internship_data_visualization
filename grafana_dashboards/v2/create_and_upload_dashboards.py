from grafanalib.core import Dashboard
from grafanalib._gen import DashboardEncoder
import json
import requests
import mysql.connector
import sys
import os

from grafanalib.core import (
    Dashboard, TimeSeries,
    GridPos, SqlTarget,
    GaugePanel, Threshold,
    BarChart,
)

#add path to sensors_fields.py and sensors_name.py
#because not in the same directory
sensors_data_path = os.environ.get('SENSORS_DATA_PATH')
if sensors_data_path is None:
    print("SENSORS_DATA_PATH environnement variable was not set")
    exit()
sys.path.insert(0, sensors_data_path)

from sensors_features import WIA_fields, fourDA_BBB_fields, fourDA_CIVIC_fields, fourDA_WIA_fields, CIVIC_fields, HiData_fields
from sensors_data import sensors
from sensors_features import sensor_areas, sensor_rooms, firebase_types

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


def sql_query(sensor_id, sensor_type, field):

    if(sensor_type == 'WIA'):
        query="SELECT " + sensor_type + "_sensor." + field + ",\
               " + sensor_type + "_sensor.time_recorded \
               FROM "   + sensor_type + "_sensor \
               WHERE "  + sensor_type + "_sensor.sensor_id = " + str(sensor_id)
    
    elif(sensor_type == 'CIVIC'):
        query="SELECT " + sensor_type + "_sensor." + field + ",\
               " + sensor_type + "_sensor.date_begin \
               FROM "   + sensor_type + "_sensor \
               WHERE "  + sensor_type + "_sensor.sensor_id = " + str(sensor_id)

    elif(sensor_type == '4DA_WIA' or sensor_type == '4DA_BBB' or sensor_type == '4DA_CIVIC'):
        query="SELECT value, " + sensor_type + "_sensor.time_recorded \
               FROM " + sensor_type + "_sensor \
               INNER JOIN " + sensor_type + "_types \
               ON " + sensor_type + "_types.id = " + sensor_type + "_sensor.type \
               WHERE " + sensor_type + "_types.name = \"" + field + "\" \
               AND " + sensor_type + "_sensor.sensor_id = " + str(sensor_id)
        
    elif(sensor_type == 'HIDATA'):
        query="SELECT HiData_sensor." + field + ",\
               HiData_sensor.time_recorded \
               FROM HiData_sensor \
               WHERE HiData_sensor.sensor_id = " + str(sensor_id)
        
    else:
        print("The sensor type is not valid")
        return None

    return query

def sql_query_avg(area_id, room_id, field):

    if(area_id != None and room_id == None):
        query="SELECT " + field + ", date_begin \
               FROM WIA_avg \
               WHERE area_id = " + str(area_id) 
        
    elif(area_id == None and room_id != None):
        query="SELECT " + field + ", date_begin \
               FROM WIA_avg \
               WHERE room_id = " + str(room_id)
        
    else:
        print("Error are and room are both null or both not null")
        return None
    
    return query
    

def dashboard_panels(sensor_id, sensor_type) : 

    #check the sensor type
    #and get the corresponding fields
    fields = []
    if(sensor_type == '4DA_WIA'):
        fields = fourDA_WIA_fields
    elif(sensor_type == '4DA_BBB'):
        fields = fourDA_BBB_fields
    elif(sensor_type == '4DA_CIVIC'):
        fields = fourDA_CIVIC_fields
    elif(sensor_type == 'HIDATA'):
        fields = HiData_fields
    elif(sensor_type == 'WIA'):
        fields = WIA_fields
    elif(sensor_type == 'CIVIC'):
        fields = CIVIC_fields
    else:
        print("The sensor type is not valid")
        return None
    
    dashboard_panels = []
    panel_number = 0
    x = 0
    for field in fields:
        query = sql_query(sensor_id, sensor_type, field)
        if(query == None):
            print("unable to create the query")
            return None
        
        if(field == 'percentage'):
            dashboard_panels.append(
                GaugePanel(
                    title = field.capitalize() + " Panel",
                    dataSource = "mysql",
                    thresholds = [Threshold('green',  0,  0.0),
                                  Threshold('yellow', 1, 50.0), 
                                  Threshold('red',    1, 80.0)],
                    targets = [
                        SqlTarget(
                            rawSql = query,
                            format = "table", 
                        )
                    ],
                    gridPos=GridPos(h=8, w=12, x=x, y=0),
                )
            )
        elif(field == 'motion'):
            dashboard_panels.append(
                BarChart(
                    title = field.capitalize() + " Panel",
                    dataSource = "mysql",
                    xTickLabelSpacing = 100, #affects the time labels
                    targets = [
                        SqlTarget(
                            rawSql = query,
                            format = "table",
                        )
                    ],
                    gridPos = GridPos(h=8, w=12, x=x, y=0),
                )
            )
        else:
            dashboard_panels.append(        
                TimeSeries(
                title = field.capitalize() + " Panel",
                dataSource = "mysql",
                targets = [
                    SqlTarget(
                        rawSql = query,
                        format = "table",
                    )
                ],
                gridPos=GridPos(h=8, w=12, x=x, y=0),
                )
            )

        #change the position of the next panel
        panel_number += 1
        if(panel_number%2 == 1):
            x = 12
        else:
            x = 0

    return dashboard_panels

def dashboard_panels_avg(area_id, room_id, sensor_type) :
    #check the sensor type
    #and get the corresponding fields
    fields = []
    if(sensor_type == 'WIA_AVG_AREA' or sensor_type == 'WIA_AVG_ROOM'):
        fields = WIA_fields
    else:
        print("The sensor type is not valid")
        return None
    
    dashboard_panels = []
    panel_number = 0
    x = 0
    for field in fields:
        query = sql_query_avg(area_id, room_id, field)
        if(query == None):
            print("unable to create the query")
            return None
        
        if(field == 'percentage'):
            dashboard_panels.append(
                GaugePanel(
                    title = field.capitalize() + " Panel",
                    dataSource = "mysql",
                    thresholds = [Threshold('green',  0,  0.0),
                                  Threshold('yellow', 1, 50.0), 
                                  Threshold('red',    1, 80.0)],
                    targets = [
                        SqlTarget(
                            rawSql = query,
                            format = "table", 
                        )
                    ],
                    gridPos=GridPos(h=8, w=12, x=x, y=0),
                )
            )
        elif(field == 'motion'):
            dashboard_panels.append(
                BarChart(
                    title = field.capitalize() + " Panel",
                    dataSource = "mysql",
                    xTickLabelSpacing = 100, #affects the time labels
                    targets = [
                        SqlTarget(
                            rawSql = query,
                            format = "table",
                        )
                    ],
                    gridPos = GridPos(h=8, w=12, x=x, y=0),
                )
            )
        else:
            dashboard_panels.append(        
                TimeSeries(
                title = field.capitalize() + " Panel",
                dataSource = "mysql",
                targets = [
                    SqlTarget(
                        rawSql = query,
                        format = "table",
                    )
                ],
                gridPos=GridPos(h=8, w=12, x=x, y=0),
                )
            )

        #change the position of the next panel
        panel_number += 1
        if(panel_number%2 == 1):
            x = 12
        else:
            x = 0

    return dashboard_panels

def dashboard_panels_firebase():

    dashboard_panels = []
    panel_number = 0
    x = 0

    for firebase_type in firebase_types:
        query = "SELECT count, time \
                 FROM Firebase_people_count \
                 INNER JOIN Firebase_types \
                 ON Firebase_types.id = Firebase_people_count.type \
                 WHERE Firebase_types.name = \"" + firebase_type + "\""
        
        dashboard_panels.append(
            GaugePanel(
                title = firebase_type.capitalize() + " Count Panel",
                dataSource = "mysql",
                targets = [
                    SqlTarget(
                        rawSql = query,
                        format = "table",
                    )
                ],
                gridPos=GridPos(h=8, w=12, x=x, y=0),
            )
        )

        #change the position of the next panel
        panel_number += 1
        if(panel_number%2 == 1):
            x = 12
        else:
            x = 0

    return dashboard_panels


def create_dashboard(sensor_name, mydb) :

    #get the sensor id and sensor type 
    mycursor = mydb.cursor()
    sql = "SELECT sensor.id, sensors_types.name FROM sensor \
           INNER JOIN sensors_types ON sensors_types.id = sensor.type \
           WHERE sensor.name = %s"
    val = (sensor_name,)

    try:
        mycursor.execute(sql, val)
    except mysql.connector.Error as err:
        print(err)
        return None
    
    result = mycursor.fetchall()
    if(len(result) == 0):
        print("Sensor name is not valid")
        return None

    sensor_id = result[0][0]
    sensor_type = result[0][1].replace("_TYPE", "")
    print(sensor_id, sensor_type)
    
    #mydb.close()

    #create the panels
    panels = dashboard_panels(sensor_id, sensor_type)
    if(panels == None):
        return None

    #create the dashboard
    dashboard = Dashboard(
        title= sensor_type + " Sensor " + str(sensor_id),
        description="dashboard for sensor " + str(sensor_id) + " data",
        tags=[
            sensor_type + ' sensor'
        ],
        timezone="browser",
        panels= panels

    ).auto_panel_ids()

    return dashboard

def create_dasboard_area(area_name, sensor_type, mydb):

    area_id = get_area_id(area_name, mydb)
    if area_id is None:
        print("The area name does not exist in the database")
        return None

    #create the panels
    panels = dashboard_panels_avg(area_id, None, sensor_type)
    if(panels == None):
        return None

    #create the dashboard
    dashboard = Dashboard(
        title= "Average for area " + area_name,
        description="average values for area " + area_name,
        tags=[
            sensor_type
        ],
        timezone="browser",
        panels= panels

    ).auto_panel_ids()

    return dashboard

def create_dasboard_room(room_name, sensor_type, mydb):

    room_id = get_room_id(room_name, mydb)
    if room_id is None:
        print("The room name does not exist in the database")
        return None

    #create the panels
    panels = dashboard_panels_avg(None, room_id, sensor_type)
    if(panels == None):
        return None

    #create the dashboard
    dashboard = Dashboard(
        title= "Average for room " + room_name,
        description="average values for room " + room_name,
        tags=[
            sensor_type
        ],
        timezone="browser",
        panels= panels

    ).auto_panel_ids()

    return dashboard

def create_dashboard_firebase(mydb):

    #create the panels
    panels = dashboard_panels_firebase()
    if(panels == None):
        print("unable to create the panels")
        return None

    #create the dashboard
    dashboard = Dashboard(
        title= "Firebase People Count",
        description="data from firebase database for people count",
        tags=[
            'FIREBASE'
        ],
        timezone="browser",
        panels= panels

    ).auto_panel_ids()

    return dashboard


def create_upload_dashboards(sensors_type, mydb):

    if(sensors_type == 'WIA_TYPE'     or sensors_type == 'CIVIC_TYPE'
    or sensors_type == 'HIDATA_TYPE'  or sensors_type == '4DA_CIVIC_TYPE' 
    or sensors_type == '4DA_WIA_TYPE' or sensors_type == '4DA_BBB_TYPE'):
        
        for sensor in sensors:
            if(sensors_type == sensor["type"]):
                sensor_name = sensor["name"]
                print(sensor_name)
                dashboard = create_dashboard(sensor_name,mydb)
                if(dashboard == None):
                    print("unable to create" + sensor_name + " dashboard")
                    continue

                my_dashboard_json = get_dashboard_json(dashboard, overwrite=True)
                upload_to_grafana(my_dashboard_json, grafana_host, grafana_api_key)
    
    elif(sensors_type == 'WIA_AVG_AREA'):
        print("WIA_AVG_AREA")
        for area_name in sensor_areas:
            dashboard = create_dasboard_area(area_name, sensors_type, mydb)
            if(dashboard == None):
                print("unable to create area " + area_name + " dashboard")
                continue

            my_dashboard_json = get_dashboard_json(dashboard, overwrite=True)
            upload_to_grafana(my_dashboard_json, grafana_host, grafana_api_key)

    elif(sensors_type == 'WIA_AVG_ROOM'):
        print("WIA_AVG_ROOM")
        for room_name in sensor_rooms:
            dashboard = create_dasboard_room(room_name, sensors_type, mydb)
            if(dashboard == None):
                print("unable to create room " + room_name + " dashboard")
                continue

            my_dashboard_json = get_dashboard_json(dashboard, overwrite=True)
            upload_to_grafana(my_dashboard_json, grafana_host, grafana_api_key)

    elif(sensors_type == 'FIREBASE_TYPE'):
        print("FIREBASE_TYPE")
        dashboard = create_dashboard_firebase(mydb)
        if(dashboard == None):
            print("unable to create firebase dashboard")
            return None

        my_dashboard_json = get_dashboard_json(dashboard, overwrite=True)
        upload_to_grafana(my_dashboard_json, grafana_host, grafana_api_key)

    else:
        print("The sensors type is not valid")
        return None


def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    '''
    get_dashboard_json generates JSON from grafanalib Dashboard object

    :param dashboard - Dashboard() created via grafanalib
    '''

    # grafanalib generates json which need to pack to "dashboard" root element
    return json.dumps(
        {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite,
            "message": message
        }, sort_keys=True, indent=2, cls=DashboardEncoder)

def upload_to_grafana(json, server, api_key, verify=True):
    '''
    upload_to_grafana tries to upload dashboard to grafana and prints response

    :param json - dashboard json generated by grafanalib
    :param server - grafana server name
    :param api_key - grafana api key with read and write privileges
    '''

    headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
    r = requests.post(f"http://{server}/api/dashboards/db", data=json, headers=headers, verify=verify)
    # TODO: add error handling
    print(f"{r.status_code} - {r.content}")


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

    #get the grafana host
    grafana_host = os.environ.get('GRAFANA_HOST')
    if grafana_host is None:
        print("GRAFANA_HOST environnement variable was not set")
        exit()

    #get the grafana api key
    grafana_api_key = os.environ.get('GRAFANA_API_KEY')
    if grafana_api_key is None:
        print("GRAFANA_API_KEY environnement variable was not set")
        exit()

    create_upload_dashboards('FIREBASE_TYPE', mydb)
    create_upload_dashboards('CIVIC_TYPE', mydb)
    create_upload_dashboards('WIA_TYPE', mydb)
    create_upload_dashboards('HIDATA_TYPE', mydb)
    create_upload_dashboards('4DA_CIVIC_TYPE', mydb)
    create_upload_dashboards('4DA_WIA_TYPE', mydb)
    create_upload_dashboards('4DA_BBB_TYPE', mydb)
    

    create_upload_dashboards('WIA_AVG_AREA', mydb)
    create_upload_dashboards('WIA_AVG_ROOM', mydb)