import mysql.connector
import WIA
import HiData
import CIVIC
import fourDA
from datetime import datetime, timedelta, timezone
from time import sleep
import os

WIA_LIMIT = 50
HIDATA_LIMIT = 5
CIVIC_LIMIT = 200
FOURDA_WIA_LIMIT = 5
FOURDA_BBB_LIMIT = 5
FOURDA_CIVIC_LIMIT = 5

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
    
    #API calls for all sensors of each category
    while True:

        #set the dates for all sensors categories
        #updated each time
        FOURDA_DATE_BEGIN = "2020-01-01"
        FOURDA_DATE_END = datetime.now().strftime("%Y-%m-%d")

        #2 hours interval to get the data for CIVIC sensors
        today = datetime.now().astimezone(timezone.utc)
        civic_date_begin = today - timedelta(hours=2)
        CIVIC_DATE_BEGIN = civic_date_begin.strftime('%Y-%m-%dT%H:%M:%SZ')
        CIVIC_DATE_END = today.strftime('%Y-%m-%dT%H:%M:%SZ')

        #API calls for each sensor category
        WIA.WIA_API_calls(WIA_LIMIT, mydb)
        HiData.HiData_API_calls(HIDATA_LIMIT, mydb)
        CIVIC.CIVIC_API_calls(CIVIC_DATE_BEGIN, CIVIC_DATE_END, CIVIC_LIMIT, mydb)
        fourDA.fourDA_API_calls(FOURDA_DATE_BEGIN, FOURDA_DATE_END,
                                FOURDA_WIA_LIMIT, FOURDA_BBB_LIMIT, FOURDA_CIVIC_LIMIT, mydb)
        
        #sleep for 1 hour
        sleep(60 * 60) 
        

