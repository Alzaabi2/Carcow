import json
import sys
import shutil

from flask import Flask, request, jsonify
from scrapeV1_1 import *
from rateV1 import *
from flask import render_template
from extension import *
from scrapeV1_6 import ScrapeAlpha
app = Flask('app')


carbrands = ['bmw', 'audi']


@app.route('/')
def index():
    return render_template("home.html")

@app.get('/cars')
def cars():
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
    url = url.replace('replaceslashes', '/')
    if 'cars' in url:
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

    tempData = []
    with open('TempData.txt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tempData.append(row)
    
    print('temp:')
    
    print(tempData[0]['Make'] + ' =? ' + singleCar['Make'])
    print(tempData[0]['Model'] + ' =? ' + singleCar['Model'])
    print(tempData[0]['Year'] + ' =? ' + singleCar['Year'])
    
    #No Zip
    if tempData[0]['Make'] == singleCar['Make'] and tempData[0]['Model'] == singleCar['Model'] and tempData[0]['Year'] == singleCar['Year']:
        del tempData[0]
        print(tempData)
        return tempData
    else:
        list = ScrapeAlpha(singleCar['Make'], singleCar['Model'], singleCar['Year'], '22201')
        rating = rate (list)
        topCars = getTopCars(list, rating)
        print('------')
        print('------')
        print(topCars)
        
        #data for last scraped car
        with open('TempData.txt', 'w', encoding='utf8', newline='') as f:
            f.write(singleCar)
            f.write(topCars)
        
        return topCars
        # [
        # {'Make':'Ford', 'Model':'Mustang', 'Year':'2016', 'Mileage':'100,000', 'Price':'20,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'Toyota', 'Model':'Supra', 'Year':'2017', 'Mileage':'101,000', 'Price':'30,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'Dodge', 'Model':'Ram', 'Year':'2018', 'Mileage':'102,000', 'Price':'40,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'BMW', 'Model':'I8', 'Year':'2019', 'Mileage':'103,000', 'Price':'50,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'Ferrari', 'Model':'445', 'Year':'2020', 'Mileage':'104,000', 'Price':'60,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'}
        # ]

app.run(host='0.0.0.0', port=8080)
