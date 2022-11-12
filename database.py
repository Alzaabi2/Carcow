import mysql.connector
from rateV1 import *


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="carcow123",
    database="CarCow"
)

def populateScraped():
    cursor = mydb.cursor()

    list = createList()
    for i in range(len(list)):
        vin   = list[i]['VIN']
        make  = list[i]['Make']
        model = list[i]['Model']
        year = list[i]['Year']
        mileage = list[i]['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)
        price = list[i]['Price']
        url   = list[i]['url']

        suggested = dollarValueVin4(vin, int(miles[0]))

        cursor.execute("INSERT INTO SCRAPED (VIN, make, model, year, mileage, price, suggested_price, url)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (vin, make, model, year, miles[0], price, suggested, url))

    mydb.commit()

    # for db in cursor:
    #     print(db)

populateScraped()