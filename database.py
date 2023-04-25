import mysql.connector
from rateV1 import *
# from scrapeV1_6_database_mass_search import *
import os
from dotenv import load_dotenv
import re

load_dotenv()

AWSPASSWORD = os.getenv('AWSPASSWORD')
APIKEY = os.getenv('CARUTILSAPIKEY')

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

    for i in list:
        # try:
        if i['VIN'] is None:
            continue
        else:
            vin   = i['VIN'][0]
        make  = i['Make']
        model = i['Model']
        trim  = i['Trim']
        # trim = ''
        year  = i['Year'].replace(' ', '')
        year2 = re.findall(r'\d+\d+', year)
        if year is None:
            print('ERROR: year is none')
            continue
        elif len(year) == 0:
            print('ERROR: year is []')
            continue

        mileage = i['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)

        price  = i['Price'].replace('$','').replace(' ','').replace(',', '')
        price2 = re.findall(r'\d+\d+', price)
        if price2 is None:
            print('ERROR: price is none')
            continue
        elif len(price2) == 0:
            print('ERROR: miles is []')
            continue

        url   = i['url']

        imageurl = i['img']
        if miles is None:
            print('ERROR: miles is none')
            continue
        elif len(miles) == 0:
            print('ERROR: miles is []')
            continue
        
        suggested = dollarValueVin4(vin, int(miles[0]))
        # print(vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl)
        try:
            cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
        except:
            print('duplicate')
        mydb.commit()
        # except:
        #     print('ERROR: insert error')
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
# print(dollarValueVin4('5J8TC1H57NL003558', 7153))