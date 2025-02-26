# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:06:49 2024

@author: Insight_DCU_Bentley
"""
import firebase_admin
from firebase_admin import credentials
#from firebase_admin import db
from firebase_admin import firestore
import mysql.connector
import os

#database connection
mydb = mysql.connector.connect(
host = "localhost",
user = "root",
password = "root",
database = "sensors"
)

# Initialize Firebase
cred = credentials.Certificate('/home/ines/internship_2ndyear/FirebaseGetData-20240802T094735Z-001/FirebaseGetData/accesstofirebase/people-counter-d8a76-firebase-adminsdk-x2rz9-888a3e64f8.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
entering_refRetrieveData = db.collection('entering')
exiting_refRetrieveData = db.collection('exiting')
people_refRetrieveData = db.collection('people')

#print('Collection:', entering_refRetrieveData)
Object_entering = entering_refRetrieveData.get()
Object_exiting = exiting_refRetrieveData.get()
Object_people = people_refRetrieveData.get()
#print('Object01:', Object01)

print("ENTERING")
for object in Object_entering:
    Document01 = object
    Data01 = Document01.get(0)
    print('Data01', Data01)

    mycursor = mydb.cursor(buffered=True)
    sql = "INSERT into Firebase_people_count \
        (type, time, count) \
        SELECT Firebase_types.id, %s, %s \
        FROM Firebase_types \
        WHERE name = %s;"
    
    val = (Data01['time'], Data01['person_id'],'entering')
    
    try :
        mycursor.execute(sql, val)
        mydb.commit()
        if(mycursor.rowcount == 0):
            print(" 0 record inserted.")
        else:
            print("1 record inserted.")

    except mysql.connector.Error as err:
        print(err)
  

print("EXITING")
for object in Object_exiting:
    Document02 = object
    Data02 = Document02.get(0)
    print('Data02', Data02)

    mycursor = mydb.cursor(buffered=True)
    sql = "INSERT into Firebase_people_count \
        (type, time, count) \
        SELECT Firebase_types.id, %s, %s \
        FROM Firebase_types \
        WHERE name = %s;"
    
    val = (Data01['time'], Data01['person_id'],'exiting')
    
    try :
        mycursor.execute(sql, val)
        mydb.commit()
        if(mycursor.rowcount == 0):
            print(" 0 record inserted.")
        else:
            print("1 record inserted.")

    except mysql.connector.Error as err:
        print(err)

print("PEOPLE")
for object in Object_people:
    Document03 = object
    Data03 = Document03.get(0)
    print('Data03', Data03)

    mycursor = mydb.cursor(buffered=True)
    sql = "INSERT into Firebase_people_count \
        (type, time, count) \
        SELECT Firebase_types.id, %s, %s \
        FROM Firebase_types \
        WHERE name = %s;"
    
    val = (Data01['time'], Data01['person_id'],'people')
    
    try :
        mycursor.execute(sql, val)
        mydb.commit()
        if(mycursor.rowcount == 0):
            print(" 0 record inserted.")
        else:
            print("1 record inserted.")

    except mysql.connector.Error as err:
        print(err)
