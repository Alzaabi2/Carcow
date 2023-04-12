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

    for i in list:
        if i['VIN'] is None:
            continue
        else:
            vin   = i['VIN']
        make  = i['Make']
        model = i['Model']
        trim  = i['Trim']
        # trim = ''
        year  = i['Year'].replace(' ', '')
        year2 = re.findall(r'\d+\d+', year)
        if len(year2) == 0:
            year2.append('-1')

        mileage = i['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)

        price  = list[i]['Price'].replace('$','').replace(' ','')
        price2 = re.findall(r'\d+\d+', price)

        url   = list[i]['url']

        imageurl = list[i]['img']

        suggested = dollarValueVin4(vin, int(miles[0]))

        cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
        mydb.commit()

        # print('its in')
        # except:
        #     print('entry error')
    print('inserted : '+ str(len(list)))
    print('example vin: '+ list[0]['VIN'])
    cursor.close()

def populateSingleScraped(i):
    cursor = mydb.cursor(buffered=True,dictionary=True)

    if i['VIN'] is None:
        return
    else:
        vin   = i['VIN']
    make  = i['Make']
    model = i['Model']
    trim  = i['Trim']
    # trim = ''
    year  = i['Year'].replace(' ', '')
    year2 = re.findall(r'\d+\d+', year)
    if len(year2) == 0:
        year2.append('-1')

    mileage = i['Mileage']
    mileage2 = mileage.replace(',','')
    miles = re.findall(r'\d+\d+', mileage2)

    price  = i['Price'].replace('$','').replace(' ','')
    price2 = re.findall(r'\d+\d+', price)

    url   = i['url']

    imageurl = i['img']

    suggested = dollarValueVin4(vin, int(miles[0]))

    cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
    mydb.commit()

        # print('its in')
        # except:
        #     print('entry error')
    print('inserted : '+ i)
    cursor.close()

# populateScraped()



# def testenv():
#     cursor = mydb.cursor(buffered=True,dictionary=True)
#     print(AWSPASSWORD)
#     cursor.execute("SELECT make FROM scraped where VIN = '19UDE2F30JA010234'")
#     print(cursor.fetchall())

# testenv()