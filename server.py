import json
from flask import Flask, request, jsonify
from scrapeV1_1 import *
from flask import render_template, request
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
    singleCarData(url) # need to create this function



app.run(host='0.0.0.0', port=8080)
