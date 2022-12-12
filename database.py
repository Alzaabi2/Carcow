import mysql.connector 
from rateV1 import *
from scrapeV1_6_database_mass_search import *
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()

AWSPASSWORD = os.getenv('AWSPASSWORD')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)

### Function that inserts a list of scraped cars into the database ###
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
        if len(miles) == 0:
            miles.append('-1')
            
        price2  = i['Price'].replace('$','').replace(' ','').replace(',', '')

        if len(price2) == 0:
            price2.append('-1')

        url   = i['url']

        imageurl = i['img']
        
        cmd = "SELECT VIN from scraped WHERE VIN = '" + vin+"'"

        cursor.execute(cmd)
        result = cursor.fetchall()
        if len(result) != 0:
            continue
        
        suggested = dollarValueVin4(vin, int(miles[0]))

        try:
            cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2, suggested, url, imageurl))
            mydb.commit()
        except:
            print("duplicate")

    print('inserted : '+ str(len(list)))
    print('example vin: '+ list[0]['VIN'])

### Function that tags cars in the database based on their availability.
# Inserts 'unavailable' or 'available' in searchID column. This makes 
# showing available cars only faster. ###
def availablity():
     cursor = mydb.cursor(dictionary=True)

     cursor.execute("SELECT * FROM scraped WHERE searchID IS NULL")
     allCars = cursor.fetchall()

     for car in range(len(allCars)):
        vin = allCars[car]['VIN']
        url = allCars[car]['url']
        available = True
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find('p', class_='sds-notification__desc') is not None:
            available = False
        elif soup.find('div', class_='text-bold text-size-600 text-size-sm-700 margin-vertical-7 margin-horizontal-7 text-center') is not None:
            if soup.find('div', class_='text-bold text-size-600 text-size-sm-700 margin-vertical-7 margin-horizontal-7 text-center').text == 'This car is no longer available. One moment while we take you to the search results page.':
                available = False
        elif soup.find('h2', class_='CVRsvD') is not None:
            available = False
        elif soup.find('h2', class_='pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0') is not None:
            if soup.find('h2', class_='pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0').text == 'Vehicle no longer available':
                available = False
        elif soup.find('div', class_='CDCXWUsedCarBuyPathExpiredListingHeaderText widget') is not None:
            available = False

        print("\navailable = ", available)
        if available != True:
            print(vin, "is unavailable")
            cursor.execute("UPDATE scraped SET SearchID = %s WHERE VIN = %s", ('unavailable', vin))
            mydb.commit()
            print("Database updated\n")
        else:
            print(vin, "is available")
            cursor.execute("UPDATE scraped SET SearchID = %s WHERE VIN = %s", ('available', vin))
            mydb.commit()
            print("Database updated\n")

availablity()



