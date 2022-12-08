import mysql.connector
from rateV1 import *
import os
from dotenv import load_dotenv

load_dotenv()

AWSPASSWORD = os.getenv('AWSPASSWORD')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)

def populateScraped(listOfScraped):
    cursor = mydb.cursor()

    list = createList()
    if len(list) == 0:
        print("List is empty")
        return

    for i in range(len(list)):
        vin   = list[i]['VIN']
        make  = list[i]['Make']
        model = list[i]['Model']
        trim  = list[i]['Trim']

        year  = list[i]['Year'].replace(' ', '')
        year2 = re.findall(r'\d+\d+', year)

        mileage = list[i]['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)

        price  = list[i]['Price'].replace('$','').replace(' ','')
        price2 = re.findall(r'\d+\d+', price)

        url   = list[i]['url']

        imageurl = list[i]['img']

        suggested = dollarValueVin4(vin, int(miles[0]))

        print("Model:", model)
        print("Trim:", trim)


        cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2[0], suggested, url, imageurl))
        mydb.commit()


    # # get vin, make, model, and trim of cars stored within the last 30 days
    # cursor.execute("SELECT VIN,make,model,trim FROM scraped WHERE DATE_SUB(CURDATE(),INTERVAL 30 DAY) <= DATE(date)")
    # test = cursor.fetchall()
    # print(test)

     
# populateScraped()



