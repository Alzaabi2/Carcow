import json
import sys
import shutil
from flask import Flask, jsonify
from flask import request as flaskRequest
from csv import writer
from rateV1 import *
from scrapeV1_6 import *
from database import *
from flask import render_template
from extension import *
from CarClass import *
import mysql.connector
import os
from dotenv import load_dotenv
from pymemcache.client import base
from contextlib import contextmanager
import threading

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
    try:
        with open('TempData.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tempData.append(row)

        with open('lastCar.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lastCar = row
    except:
        with open('lastCar.txt', 'w', encoding='utf8', newline='\n') as f:
            w = writer(f)
            header = ['make', 'model', 'year', 'Zip']
            w.writerow(header)
            #no rip
            row = ['sample', 'sample', '2023', '22201']
            w.writerow(row)
            
        with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
            w = writer(f)
            header = ['VIN', 'make', 'model', 'year', 'trim', 'mileage', 'price', 'suggested', 'url', 'imageurl']
            w.writerow(header)
            for i in range(len(topCars)):
                row = ['sample', 'sample', 'sample', 'sample', 'sample', 'sample', 'sample', 'sample', 'sample', 'sample']
                w.writerow(row)

    if lastCar != {}:  
        if lastCar['make'] == singleCar['make'] and lastCar['model'] == singleCar['model'] and float(lastCar['year']) == float(singleCar['year']):
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

@app.route('/getCarData/<string:make>/<string:model>/<string:year>/<string:zip>/<int:pricePriority>/<int:mileagePriority>/<int:lowestYear>/<int:highestYear>/<string:trim>/<int:trimPriority>')
def getCarData(make, model, year, zip, pricePriority, mileagePriority, lowestYear, highestYear, trim, trimPriority):
    cursor = mydb.cursor(dictionary=True)

    if pricePriority == mileagePriority == yearPriority == trimPriority:
        pricePriority = 1
        mileagePriority = 1
        yearPriority = 1
        trimPriority = 1

    #Check if the user searched for the same car, by checking memcached
    # Don't forget to run `memcached' before running this next line:
    client = base.Client(('localhost', 11211))
    searchID = model+year+str(pricePriority)+str(mileagePriority)+str(lowestYear)+str(highestYear)+trim+str(trimPriority)
    print("Search ID: ", searchID, " Type of searchID: ", type(searchID))

    cars = client.get(searchID)
        
    if cars is not None:
        cars = cars.decode('utf-8').replace(" '", " \"").replace("':", "\":").replace("{'", "{\"").replace("',", "\",").replace("None", "\"\"").replace('datetime.datetime', '"datetime.datetime').replace(")", ")\"")
        print(cars)
        topCars = json.loads(cars)

        print("\nFound list of cars in memcache")
        cursor.close()
        return topCars
    
    #Searched car is not in memcached, pull from database, rate, and send first 5 checked, then continue checking

    year = float(year)
    yearUp = year + 2
    yearDown = year - 2

    if lowestYear != 0 or highestYear != 0:
        if lowestYear != 0 and highestYear == 0:
            yearDown = lowestYear
        elif lowestYear == 0 and highestYear != 0:
            yearUp = highestYear
        elif lowestYear != 0 and highestYear != 0:
            yearDown = lowestYear
            yearUp = highestYear

    
    cursor.execute("SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s) AND date >= '2023-02-00'", (model, yearUp, yearDown, 'available'))

    list = cursor.fetchall()
    print("\nThe length of the original list of cars: ", len(list))

    #TO-DO
    #color = colorRating(list, color, colorRate)
    #distance = distanceRating(list, distanceRate)

    price = priceRating(list)
    mileage = mileageRating(list)
    year = yearRating(list, year)
    trim = trimRating(list, trim.replace('_', ' '))

    vin_dict = {}
    
    for vin, price_rating, url in price:
        vin_dict[vin] = {"price": price_rating, "url": url}
    
    for vin, mile_rating in mileage:
        if vin in vin_dict:
            vin_dict[vin]["mileage"] = mile_rating

    for vin, year_rating in year:
        if vin in vin_dict:
            vin_dict[vin]["year"] = year_rating
    
    for vin, trim_rating in trim:
        if vin in vin_dict:
            vin_dict[vin]["trim"] = trim_rating
    
    combined_list = [(vin, vin_dict[vin]["price"], vin_dict[vin]["url"], vin_dict[vin]["mileage"], vin_dict[vin]["year"], vin_dict[vin]["trim"]) for vin in vin_dict]
    
    rating = preferenceRate(combined_list, pricePriority, mileagePriority, trimPriority)

    sortedList = getTopCars(list, rating)
    

    topCars = []
    availableCounter = 0
    t = threading.Thread(target = maintainence, args = (searchID, sortedList))
    t.setDaemon(False)
    t.start()
    ("Thread Started")

    for i in range(len(sortedList)):
        if availableCounter == 5:
            availableCounter += 1
            print("\nThe 5 top cars returned to chrome extension: ", topCars)
            cursor.close()
            return topCars
        if checkAvailability(sortedList[i]['url']):
            if "https:" not in sortedList[i]['imageurl']:
                sortedList[i]['imageurl'] = "https:" + sortedList[i]['imageurl']
            topCars.append(sortedList[i])
            availableCounter += 1
            #Set the memcache for the list of cars
            client.set(searchID, topCars, 60*60*6)

    print("\n The length of the final list of available cars: ", len(topCars))
    cursor.close()
    return topCars

def maintainence(searchID, sortedList):
    topCars = []
    client = base.Client(('localhost', 11211))
    print("Inside thread function")
    for i in range(len(sortedList)):
        if checkAvailability(sortedList[i]['url']):
            if "https:" not in sortedList[i]['imageurl']:
                sortedList[i]['imageurl'] = "https:" + sortedList[i]['imageurl']
            topCars.append(sortedList[i])
            #Set the memcache for the list of cars
            client.set(searchID, topCars, 60*60*6)

    print("Final list of checked cars", topCars)

    return topCars

# @app.route('/addCurrent/<string:vin>/<string:make>/<string:model>/<string:year>/<string:trim>/<string:mileage>/<string:price>/<string:url>/<string:imageurl>')
@app.route('/addCurrent', methods=['POST'])
def addCurrent():
# def addCurrent(vin, make, model, year, trim, mileage, price, url, imageurl):
    data = flaskRequest.get_json()
    print(data)
   
    cursor = mydb.cursor(dictionary=True)

    cursor.execute("SELECT * FROM scraped WHERE VIN = %s", (data['VIN'],))
    list = cursor.fetchall()

    if list:
        print("Current car already in database:\n")
        print("\n", list, "\n")
        cursor.close()
        return ""
    else:
        print("Current car not in database, adding to database\n")
        car_dict = {
            "VIN": data['VIN'],
            "Make": data['make'],
            "Model": data['model'],
            "Year": data['year'],
            "Trim": data['trim'],
            "Mileage": data['mileage'],
            "Price": data['price'],
            "url": data['url'],
            "img": data['imgURL']
        }

        car_list = []
        car_list.append(car_dict)

        cursor.close()
        populateSingleScraped(car_dict)

    print("Current car added to databse\n")
    
    print('database connection error')

    return ""

@app.route('/findEquivalent/<string:model>/<string:year>/<int:pricePriority>/<int:mileagePriority>/<int:lowestYear>/<int:highestYear>/<string:trim>/<int:trimPriority>')
def findEquivalent(model, year, pricePriority, mileagePriority, lowestYear, highestYear, trim, trimPriority):
    cursor = mydb.cursor(dictionary=True)

    if pricePriority == mileagePriority == yearPriority == trimPriority:
        pricePriority = 1
        mileagePriority = 1
        yearPriority = 1
        trimPriority = 1

    #Check if the user searched for the same car, by checking memcached
    # Don't forget to run `memcached' before running this next line:

    model = model.lower()
    print(model)

    try:
        model = globals()[model]
    except:
        print("\nModel class not available\n")
        return

    modelClass = model.model_class

    client = base.Client(('localhost', 11211))
    searchID = modelClass.replace(" ", "")+year+str(pricePriority)+str(mileagePriority)+ str(lowestYear) + str(highestYear) + trim +str(trimPriority)
    print("Search ID: ", searchID, " Type of searchID: ", type(searchID))

    cars = client.get(searchID)
        
    if cars is not None:
        cars = cars.decode('utf-8').replace(" '", " \"").replace("':", "\":").replace("{'", "{\"").replace("',", "\",").replace("None", "\"\"").replace('datetime.datetime', '"datetime.datetime').replace(")", ")\"")
        print(cars)
        topCars = json.loads(cars)

        print("\nFound list of cars in memcache")
        cursor.close()
        return topCars
    
    #Searched car is not in memcached, pull from database, rate, and send first 5 checked, then continue checking
    
    sameClassModels = []

    if model in models_list:
        for model in models_list:
            if model.model_class == modelClass:
                sameClassModels.append(model.name)
    else:
        sameClassModels.append(model)

    print("\nModels of same class:\n", sameClassModels, "\n")

    year = float(year)
    yearUp = year + 2
    yearDown = year - 2

    if lowestYear != 0 or highestYear != 0:
        if lowestYear != 0 and highestYear == 0:
            yearDown = lowestYear
        elif lowestYear == 0 and highestYear != 0:
            yearUp = highestYear
        elif lowestYear != 0 and highestYear != 0:
            yearDown = lowestYear
            yearUp = highestYear

    combined_results = []

    # Loop through the list of models and execute the query for each model
    for model in sameClassModels:
        # Generate query for each model
        query = "SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s) AND date >= '2023-02-00'"
        
        # Execute the query against the database
        cursor.execute(query, (model, yearUp, yearDown, 'available'))
        
        # Fetch the results and append them to the combined results list
        results = cursor.fetchall()
        combined_results.extend(results)


    print("\nCars from database of type", modelClass, ":\n", combined_results, "\n")

    #TO-DO
    #color = colorRating(list, color, colorRate)
    #distance = distanceRating(list, distanceRate)

    price = priceRating(combined_results)
    mileage = mileageRating(combined_results)
    year = yearRating(combined_results, year)
    trim = trimRating(combined_results, trim.replace('_', ' '))

    vin_dict = {}
    
    for vin, price_rating, url in price:
        vin_dict[vin] = {"price": price_rating, "url": url}
    
    for vin, mile_rating in mileage:
        if vin in vin_dict:
            vin_dict[vin]["mileage"] = mile_rating

    for vin, year_rating in year:
        if vin in vin_dict:
            vin_dict[vin]["year"] = year_rating
    
    for vin, trim_rating in trim:
        if vin in vin_dict:
            vin_dict[vin]["trim"] = trim_rating
    
    combined_list = [(vin, vin_dict[vin]["price"], vin_dict[vin]["url"], vin_dict[vin]["mileage"], vin_dict[vin]["year"], vin_dict[vin]["trim"]) for vin in vin_dict]
    
    rating = preferenceRate(combined_list, pricePriority, mileagePriority, trimPriority)

    sortedList = getTopCars(combined_results, rating)
    

    topCars = []
    availableCounter = 0
    t = threading.Thread(target = maintainence, args = (searchID, sortedList))
    t.setDaemon(False)
    t.start()
    ("Thread Started")

    for i in range(len(sortedList)):
        if availableCounter == 5:
            availableCounter += 1
            print("\nThe 5 top cars returned to chrome extension: ", topCars)
            cursor.close()
            return topCars
        if checkAvailability(sortedList[i]['url']):
            if "https:" not in sortedList[i]['imageurl']:
                sortedList[i]['imageurl'] = "https:" + sortedList[i]['imageurl']
            topCars.append(sortedList[i])
            availableCounter += 1
            #Set the memcache for the list of cars
            client.set(searchID, topCars, 60*60*6)

    print("\n The length of the final list of available cars: ", len(topCars))
    cursor.close()
    return topCars







### WHEEL DEAL ANDROID APP ###
@app.route('/getCarDataApp/<string:make>/<string:model>/<string:year>/<string:zip>/<int:pricePriority>/<int:mileagePriority>/<int:yearPriority>/<string:trim>/<int:trimPriority>')
def getCarDataApp(make, model, year, zip, pricePriority, mileagePriority, yearPriority, trim, trimPriority):
    cursor = mydb.cursor(dictionary=True)

    if pricePriority == mileagePriority == yearPriority == trimPriority:
        pricePriority = 1
        mileagePriority = 1
        yearPriority = 1
        trimPriority = 1

    #Check if the user searched for the same car, by checking memcached
    # Don't forget to run `memcached' before running this next line:
    client = base.Client(('localhost', 11211))
    searchID = model+year+str(pricePriority)+str(mileagePriority)+str(yearPriority)+trim+str(trimPriority)
    print("Search ID: ", searchID, " Type of searchID: ", type(searchID))

    cars = client.get(searchID)
        
    if cars is not None:
        cars = cars.decode('utf-8').replace(" '", " \"").replace("':", "\":").replace("{'", "{\"").replace("',", "\",").replace("None", "\"\"").replace('datetime.datetime', '"datetime.datetime').replace(")", ")\"")
        print(cars)
        topCars = json.loads(cars)

        print("\nFound list of cars in memcache")
        cursor.close()
        return topCars
    
    #Searched car is not in memcached, pull from database, rate, and send first 5 checked, then continue checking

    year = float(year)
    yearUp = year + 2
    yearDown = year - 2
    
    cursor.execute("SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s) AND date >= '2023-02-00'", (model, yearUp, yearDown, 'available'))

    list = cursor.fetchall()
    print("\nThe length of the original list of cars: ", len(list))

    #TO-DO
    #color = colorRating(list, color, colorRate)
    #distance = distanceRating(list, distanceRate)

    price = priceRating(list)
    mileage = mileageRating(list)
    year = yearRating(list, year)
    trim = trimRating(list, trim.replace('_', ' '))

    vin_dict = {}
    
    for vin, price_rating, url in price:
        vin_dict[vin] = {"price": price_rating, "url": url}
    
    for vin, mile_rating in mileage:
        if vin in vin_dict:
            vin_dict[vin]["mileage"] = mile_rating

    for vin, year_rating in year:
        if vin in vin_dict:
            vin_dict[vin]["year"] = year_rating
    
    for vin, trim_rating in trim:
        if vin in vin_dict:
            vin_dict[vin]["trim"] = trim_rating
    
    combined_list = [(vin, vin_dict[vin]["price"], vin_dict[vin]["url"], vin_dict[vin]["mileage"], vin_dict[vin]["year"], vin_dict[vin]["trim"]) for vin in vin_dict]
    
    rating = preferenceRate(combined_list, pricePriority, mileagePriority, trimPriority)

    sortedList = getTopCars(list, rating)
    

    topCars = []
    availableCounter = 0
    t = threading.Thread(target = maintainence, args = (searchID, sortedList))
    t.setDaemon(False)
    t.start()
    ("Thread Started")

    for i in range(len(sortedList)):
        if availableCounter == 5:
            availableCounter += 1
            print("\nThe 5 top cars returned to chrome extension: ", topCars)
            cursor.close()
            return topCars
        if checkAvailability(sortedList[i]['url']):
            if "https:" not in sortedList[i]['imageurl']:
                sortedList[i]['imageurl'] = "https:" + sortedList[i]['imageurl']
            topCars.append(sortedList[i])
            availableCounter += 1
            #Set the memcache for the list of cars
            client.set(searchID, topCars, 60*60*6)

    print("\n The length of the final list of available cars: ", len(topCars))
    cursor.close()
    return topCars

#getPreferences(0,2,3,'NA',0)
# getCarData('hyundai', 'palisade','2020','22182',10,0,0,'NA',0)

# findEquivalent("corolla",'2020',0,0,0,'NA',0)

app.run(host='0.0.0.0', port=8080)