import mysql.connector
from rateV1 import *
# from scrapeV1_6_database_mass_search import *
import os
from dotenv import load_dotenv
import re

load_dotenv()

AWSPASSWORD = os.getenv('AWSPASSWORD')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)

def populateScraped(list):
    cursor = mydb.cursor(buffered=True,dictionary=True)

    # list = createList()
    if len(list) == 0 or list is None:
        print("List is empty")
        return

    for i in range(len(list)):
        if list[i]['VIN'] is None:
            continue
        else:
            vin   = list[i]['VIN']
        make  = list[i]['Make']
        model = list[i]['Model']
        trim  = list[i]['Trim']
        # trim = ''
        year  = list[i]['Year'].replace(' ', '')
        year2 = re.findall(r'\d+\d+', year)
        if len(year2) == 0:
            year2.append('-1')

        mileage = list[i]['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)

        price  = list[i]['Price'].replace('$','').replace(' ','')
        price2 = re.findall(r'\d+\d+', price)

        url   = list[i]['url']

        imageurl = list[i]['img']

        if(len(miles) == 0):
            continue
        suggested = dollarValueVin4(vin, int(miles[0]))
        if suggested == 'duplicate':
            print('duplicate')
            continue
        if len(year2)==0 or len(miles)==0 or len(price2)==0:
            continue
        cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
        mydb.commit()

        # print('its in')
        # except:
        #     print('entry error')
    print('inserted : '+ str(len(list)))
    print('example vin: '+ list[0]['VIN'])

# populateScraped()



# def testenv():
#     cursor = mydb.cursor(buffered=True,dictionary=True)
#     print(AWSPASSWORD)
#     cursor.execute("SELECT make FROM scraped where VIN = '19UDE2F30JA010234'")
#     print(cursor.fetchall())

# testenv()