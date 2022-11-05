import json
import sys
import shutil

from flask import Flask, request, jsonify
from scrapeV1_1 import *
from rateV1 import *
from flask import render_template
from extension import *
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
    # if url == '':
    #     print('n')
    #     return
    url2 = 'https://www.cars.com/vehicledetail/' + url
    # print(url2)
    singleCar = singleCarData(url2) # need to create this function
    Scrape(singleCar['Make'], singleCar['Model'], singleCar['Year'], '22201')
    list = createList()
    rating = rate (list)
    topCars = getTopCars(list, rating)
    print(topCars)
    
    return topCars
        # [
        # {'Make':'Ford', 'Model':'Mustang', 'Year':'2016', 'Mileage':'100,000', 'Price':'20,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'Toyota', 'Model':'Supra', 'Year':'2017', 'Mileage':'101,000', 'Price':'30,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'Dodge', 'Model':'Ram', 'Year':'2018', 'Mileage':'102,000', 'Price':'40,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'BMW', 'Model':'I8', 'Year':'2019', 'Mileage':'103,000', 'Price':'50,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'},
        # {'Make':'Ferrari', 'Model':'445', 'Year':'2020', 'Mileage':'104,000', 'Price':'60,000', 'url':'https://www.cars.com/vehicledetail/92a80785-7bf4-42fc-b7dd-5365633f054e/'}
        # ]

app.run(host='0.0.0.0', port=8080)
