import json
import sys
import shutil

from flask import Flask, request, jsonify
from scrapeV1_1 import *
from rateV1 import *
from flask import render_template
from extension import *
from scrapeV1_6 import ScrapeAlpha, cleanData
import mysql.connector
app = Flask('app')


carbrands = ['bmw', 'audi']

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Hevcy4-gumden-wypjav",
    database="CarCowDB"
)

@app.route('/')
def index():
    return render_template("home.html")

@app.get('/cars')
def cars():
    print("called")
    return {'car brands' : carbrands}

@app.route('/year/<int:car_year>')
def getYear(car_year):
    print(car_year)
    return render_template("home.html")
    
@app.route('/scrape/<string:make>/<string:model>/<string:car_year>/<string:zip>')
def getScrape(make, model, car_year, zip):
    Scrape(make, model, car_year, zip)
    print('scraped', make, model, car_year, zip)
    return render_template("home.html")

@app.route('/getUrl/<string:url>')
def getUrl(url):
    cursor = mydb.cursor(dictionary=True)

    time1 = time.perf_counter()
    url = url.replace('slash', '/')
    url = url.replace('colum', ':')
    url = url.replace('dot', '.')
    print(url)
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
    print('website found: ' + url)

    time2 = time.perf_counter()
    print("Timer1 singleCar():" + str(time2-time1))
    
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

    
    # print('temp:')
    
    # print(tempData[0]['Make'] + ' =? ' + singleCar['Make'])
    # print(tempData[0]['Model'] + ' =? ' + singleCar['Model'])
    # print(tempData[0]['Year'] + ' =? ' + singleCar['Year'])
    
   
    # No Zip
    print(lastCar)
    print('tempdata ^ single car v')
    print(singleCar)
    # if lastCar != {}:  
    #     if lastCar['Make'] == singleCar['Make'] and lastCar['Model'] == singleCar['Model'] and lastCar['Year'] == singleCar['Year']:
    #         print(tempData)
    #         return tempData

    time3 = time.perf_counter()
    print("Timer2 tempData:" + str(time3-time2))


    # list = ScrapeAlpha(singleCar['Make'], singleCar['Model'], singleCar['Year'], '22201')
    print(singleCar['Make'])
    cursor.execute("SELECT * FROM scraped WHERE make = %s", (singleCar['Make'],))
    list = cursor.fetchall()
    print(list)
    time4 = time.perf_counter()
    print("Timer3 ScrapeAlpha():" + str(time4-time3))
    
    # list = cleanData(list)
    time5 = time.perf_counter()
    print("Timer4 cleanData():" + str(time5-time4))
    
    rating = rate3(list)
    time6 = time.perf_counter()
    print("Timer5 rate:" + str(time6-time5))
    
    topCars = getTopCars(list, rating)
    time7 = time.perf_counter()
    print("Timer6 topCars():" + str(time7-time6))
    
    print('------')
    print('------')
    print(topCars)
    
    #data for last scraped car
    with open('lastCar.txt', 'w', encoding='utf8', newline='\n') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Zip']
        w.writerow(header)
        #no rip
        row = [singleCar['Make'], singleCar['Model'], singleCar['Year'], '22201']
        w.writerow(row)
        
    with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        for i in range(len(topCars)):
            row = [topCars[i]['make'], topCars[i]['model'], topCars[i]['year'], topCars[i]['mileage'], topCars[i]['price'], topCars[i]['VIN'], topCars[i]['url']]
            w.writerow(row)
    
    # topCars = [
    # {'Make':'Ford', 'Model':'Mustang', 'Year':'2016', 'Mileage':'100,000', 'Price':'20,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
    # {'Make':'Toyota', 'Model':'Supra', 'Year':'2017', 'Mileage':'101,000', 'Price':'30,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
    # {'Make':'Dodge', 'Model':'Ram', 'Year':'2018', 'Mileage':'102,000', 'Price':'40,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
    # {'Make':'BMW', 'Model':'I8', 'Year':'2019', 'Mileage':'103,000', 'Price':'50,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
    # {'Make':'Ferrari', 'Model':'445', 'Year':'2020', 'Mileage':'104,000', 'Price':'60,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'}
    # ]
    time8 = time.perf_counter()
    print("Timer7 tempDataWrite:" + str(time8-time7))
    return topCars

app.run(host='0.0.0.0', port=8080)
