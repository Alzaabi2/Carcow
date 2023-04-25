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
            vin   = i['VIN']
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
        query = 'SELECT * FROM scraped WHERE `VIN` = "'+vin+'"'
        cursor.execute(query)
        prevListing = cursor.fetchall()
        # print('prev listing')
        # print(prevListing)
        found = False
        if prevListing != [] and prevListing != None:
            # if prevListing[0]['searchID'] == 'unavailable':
            query = 'DELETE FROM scraped WHERE `VIN` = "'+vin+'"'
            cursor.execute(query)
            print('removing previous listing')
            # else:
                # if (checkAvailability(prevListing[0]['url'])) == False:
                #     query = 'DELETE FROM scraped WHERE `VIN` = "'+vin+'"'
                #     cursor.execute(query)
                #     print('removing previous listing: unavailable')
                # else:
                #     found = True
                #     print('dup found')
        # # try:
        # if found == False:
        #     # if('https://' not in imageurl):
        #     #     imageurl = 'https://'+imageurl
        #     print((vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
        cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
        # # except:
        # #     print('duplicate')
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
def massAvailabilityCheck():
    cursor = mydb.cursor(buffered=True,dictionary=True)
    query = 'SELECT * FROM scraped WHERE searchID != "unavailable" or searchID is NULL'
    cursor.execute(query)
    listings = cursor.fetchall()
    print(str(len(listings)))
    counter = 0
    for i in listings:
        print('count :' +str(counter))
        if checkAvailability(i['url']) == False:
            query2 = 'UPDATE scraped SET searchID = "unavailable" WHERE VIN = "'+i['VIN']+'";'
            cursor.execute(query2)
            mydb.commit()
        counter+=1
# massAvailabilityCheck()