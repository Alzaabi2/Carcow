import json
import sys
import shutil
from flask import Flask, request, jsonify
from csv import writer
from rateV1 import *
from scrapeV1_6 import *
from flask import render_template
from extension import *
from scrapeV1_6 import ScrapeAlpha, cleanData
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
AWSPASSWORD = os.getenv('AWSPASSWORD')

app = Flask('app')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/year/<int:car_year>')
def getyear(car_year):
    return render_template("home.html")
    
@app.route('/scrape/<string:make>/<string:model>/<string:car_year>/<string:zip>')
def getScrape(make, model, car_year, zip):
    Scrape1(make, model, car_year, zip)
    return render_template("home.html")

@app.route('/getUrl/<string:url>')
def getUrl(url):
    cursor = mydb.cursor(dictionary=True)

    time1 = time.perf_counter()
    url = url.replace('slash', '/')
    url = url.replace('colum', ':')
    url = url.replace('dot', '.')
    url = url.replace('questionmark', '?')
    url = url.replace('constautotraderurl', 'https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml')
    
    if 'cars.com' in url:
        singleCar = singleCarData1(url)
    elif 'autotrader' in url:
        singleCar = singleCarData2(url)
    elif 'cargurus' in url:
        singleCar = singleCarData3(url)
    elif 'edmunds' in url:
        singleCar = singleCarData4(url)
    elif 'carsdirect' in url:
        singleCar = singleCarData5(url)
    else:
        print('unregistered website')
        return 'unregistered website'

    print('\n1. URL from current window recieved and data of current car viewed retrieved \n')

    time2 = time.perf_counter()
    # print("Timer1 singleCar():" + str(time2-time1))
    
    tempData = []
    lastCar = {}

    with open('TempData.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tempData.append(row)

    with open('lastCar.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lastCar = row

    if lastCar != {}:  
        if lastCar['make'] == singleCar['make'] and lastCar['model'] == singleCar['model'] and lastCar['year'] == singleCar['year']:
            for i in range(len(tempData)):
                if "https:" not in tempData[i]['imageurl']:
                    tempData[i]['imageurl'] = "https:" + tempData[i]['imageurl']
            print("\n2. Same car as last search, return previous output.\n")
            print("\nDone.\n")
            return tempData

    time3 = time.perf_counter()
    # print("Timer2 tempData:" + str(time3-time2))

    year = float(singleCar['year'])
    yearUp = year + 2
    yearDown = year - 2
    cursor.execute("SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s)", (singleCar['model'], yearUp, yearDown, 'available'))

    list = cursor.fetchall()
    print("\n2. Fetched data of similar cars from database \n")
    time4 = time.perf_counter()
    # print("Timer3 ScrapeAlpha():" + str(time4-time3))
    
    time5 = time.perf_counter()
    # print("Timer4 cleanData():" + str(time5-time4))
    
    rating = rate2(list)
    print("\n3. Rating of fetched data is done.\n")
    time6 = time.perf_counter()
    # print("Timer5 rate:" + str(time6-time5))
    
    topCars = getTopCars(list, rating)
    print("\n4. From the list of the rated cars, the top 5 are retrieved, with all relevant data from the database \n")
    time7 = time.perf_counter()
    # print("Timer6 topCars():" + str(time7-time6))
    
    #data for last scraped car
    with open('lastCar.txt', 'w', encoding='utf8', newline='\n') as f:
        w = writer(f)
        header = ['make', 'model', 'year', 'Zip']
        w.writerow(header)
        #no rip
        row = [singleCar['make'], singleCar['model'], singleCar['year'], '22201']
        w.writerow(row)
        
    with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
        w = writer(f)
        header = ['VIN', 'make', 'model', 'year', 'trim', 'mileage', 'price', 'suggested', 'url', 'imageurl']
        w.writerow(header)
        for i in range(len(topCars)):
            row = [topCars[i]['VIN'], topCars[i]['make'], topCars[i]['model'], topCars[i]['year'], topCars[i]['trim'], topCars[i]['mileage'], topCars[i]['price'], topCars[i]['suggested'], topCars[i]['url'], topCars[i]['imageurl']]
            w.writerow(row)
    
    time8 = time.perf_counter()
    # print("Timer7 tempDataWrite:" + str(time8-time7))

    for i in range(len(topCars)):
        # print(topCars[i]['imageurl'])
        if "https:" not in topCars[i]['imageurl']:
            topCars[i]['imageurl'] = "https:" + topCars[i]['imageurl']
    print("\n5. The top 5 cars are returned to Chrome extension.\n")
    print("\nDone.\n")

    return topCars

app.run(host='0.0.0.0', port=8080)
