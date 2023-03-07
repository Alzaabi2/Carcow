from dotenv import load_dotenv
import os
import mysql.connector
from pymemcache.client import base
import json
from rateV1 import *


load_dotenv()
AWSPASSWORD = os.getenv('AWSPASSWORD')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)

def setData(userID, model, year):
    cursor = mydb.cursor(dictionary=True)
     
    year = float(year)
    yearUp = year + 2
    yearDown = year - 2
    cursor.execute("SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s) LIMIT 15", (model, yearUp, yearDown, 'available'))

    list = cursor.fetchall()

    # Don't forget to run `memcached' before running this next line:
    client = base.Client(('localhost', 11211))
    
    # Once the client is instantiated, you can access the cache:
    client.set(userID, list, 60*60*6)
    
    for i in range(len(list)):
        print(list[i])

def getData(userID):
    # Don't forget to run `memcached' before running this next line:
    client = base.Client(('localhost', 11211))

    # Retrieve previously set data again:
    value = client.get(userID).decode('utf-8').replace(" '", " \"").replace("':", "\":").replace("{'", "{\"").replace("',", "\",").replace("None", "\"\"").replace('datetime.datetime', '"datetime.datetime').replace(")", ")\"")
    # print(value)
    v = json.loads(value)

    # value = client.get(userID)

    list = []

    # for i in range(len(v)):
    #     list.append(v[i])
    
    # print(v[9]['year'])
    print(v)
    # print(value)
    # print(list[0][])


#setData('100', 'wrangler', '2019')
getData("palisade2020111NA1")