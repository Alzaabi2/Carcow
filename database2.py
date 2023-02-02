import mysql.connector
from rateV1 import *
import os
from dotenv import load_dotenv

load_dotenv()


mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Hevcy4-gumden-wypjav",
    database="CarCowDB"
)

def populateScraped():
    cursor = mydb.cursor()

    list = createList()
    for i in range(len(list)):
        vin   = list[i]['VIN']
        make  = list[i]['Make']
        modelAndTrim = list[i]['Model']
        year = list[i]['Year']
        mileage = list[i]['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)
        price = list[i]['Price']
        url   = list[i]['url']

        suggested = dollarValueVin4(vin, int(miles[0]))

        allWords = modelAndTrim.split(' ',1)
        model = allWords[0]
        trim = allWords[1]

        cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year, trim, miles[0], price, suggested, url))

    # cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", ('2C3CDZFJ6LH243418', 'Dodge','Challenger', '2020', 'R/T Scat Pack', '34,873 mi.',"$42,966", '43,000', 'http://cars.com/vehicledetail/fa69f331-94f7-409e-8e3d-660257f51bf9/'))
    mydb.commit()



