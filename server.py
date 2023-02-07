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

#@app.route('/getPreferences/<int:pricePriority>/<int:mileagePriority>/<int:yearPriority>/<string:trim>/<int:trimPriority>')
def getPreferences(pricePriority, mileagePriority, yearPriority, trim, trimPriority):
    cursor = mydb.cursor(dictionary=True)

    print(pricePriority, mileagePriority, yearPriority, trim, trimPriority)

    with open('lastCar.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lastCar = row
    
    cursor.execute("SELECT * FROM scraped WHERE model = %s AND (searchID IS NULL OR searchID = %s) AND date >= '2023-02-00'", (lastCar['model'], 'available'))
    
    list = cursor.fetchall()
    
    # print(list, "\n")

    #TO-DO
    #color = colorRating(list, color, colorRate)
    #distance = distanceRating(list, distanceRate)


    price = priceRating(list)
    mileage = mileageRating(list)
    year = yearRating(list, lastCar['year'])
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
    # print(combined_list, "\n")
    
    rating = preferenceRate(combined_list, pricePriority, mileagePriority, yearPriority, trimPriority)
    
    topCars = getTopCars(list, rating)
    # print(topCars)

    for i in range(len(topCars)):
        # print(topCars[i]['imageurl'])
        if "https:" not in topCars[i]['imageurl']:
            topCars[i]['imageurl'] = "https:" + topCars[i]['imageurl']
    
    return topCars

@app.route('/getCarData/<string:make>/<string:model>/<string:year>/<string:zip>/<int:pricePriority>/<int:mileagePriority>/<int:yearPriority>/<string:trim>/<int:trimPriority>')
def getCarData(make,model,year,zip, pricePriority, mileagePriority, yearPriority, trim, trimPriority):
    cursor = mydb.cursor(dictionary=True)

    if pricePriority + mileagePriority + yearPriority + trimPriority == 0:
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
            if lastCar['make'] == make and lastCar['model'] == model and float(lastCar['year']) == float(year):
                for i in range(len(tempData)):
                    if "https:" not in tempData[i]['imageurl']:
                        tempData[i]['imageurl'] = "https:" + tempData[i]['imageurl']
                print("\n2. Same car as last search, return previous output.\n")
                print("\nDone.\n")
                return tempData

        time3 = time.perf_counter()
        # print("Timer2 tempData:" + str(time3-time2))

        #error check for undefined data
        if(year == 'undefined'):
            return tempData
        
        year = float(year)
        yearUp = year + 2
        yearDown = year - 2
        cursor.execute("SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s)", (model, yearUp, yearDown, 'available'))

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
            row = [make, model, year, '22201']
            w.writerow(row)
            
        with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
            w = writer(f)
            header = ['VIN', 'make', 'model', 'year', 'trim', 'mileage', 'price', 'suggested', 'url', 'imageurl']
            w.writerow(header)
            for i in range(len(topCars)):
                row = [topCars[i]['VIN'], topCars[i]['make'], topCars[i]['model'], topCars[i]['year'], topCars[i]['trim'], topCars[i]['mileage'], topCars[i]['price'], topCars[i]['suggested'], topCars[i]['url'], topCars[i]['imageurl']]
                w.writerow(row)

        if lastCar != {}:
            print(lastCar['make'], '!=?', make)
            print(lastCar['model'], '!=?', model)
            print(lastCar['year'], '!=?', year)
            if lastCar['make'] == make and lastCar['model'] == model and float(lastCar['year']) == float(year):
                for i in range(len(tempData)):
                    if "https:" not in tempData[i]['imageurl']:
                        tempData[i]['imageurl'] = "https:" + tempData[i]['imageurl']
                print("\n2. Same car as last search, return previous output.\n")
                print("\nDone.\n")
                return tempData

        time3 = time.perf_counter()
        # print("Timer2 tempData:" + str(time3-time2))

        year = float(year)
        yearUp = year + 2
        yearDown = year - 2
        cursor.execute("SELECT * FROM scraped WHERE model = %s AND (year <= %s AND year >= %s) AND (searchID IS NULL OR searchID = %s)", (model, yearUp, yearDown, 'available'))

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
            row = [make, model, str(year), '22201']
            w.writerow(row)
            
        with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
            w = writer(f)
            header = ['VIN', 'make', 'model', 'year', 'trim', 'mileage', 'price', 'suggested', 'url', 'imageurl']
            w.writerow(header)
            for i in range(len(topCars)):
                row = [topCars[i]['VIN'], topCars[i]['make'], topCars[i]['model'], str(topCars[i]['year']), topCars[i]['trim'], str(topCars[i]['mileage']), str(topCars[i]['price']), str(topCars[i]['suggested']), topCars[i]['url'], topCars[i]['imageurl']]
                w.writerow(row)
        
        time8 = time.perf_counter()
        # print("Timer7 tempDataWrite:" + str(time8-time7))

        for i in range(len(topCars)):
            # print(topCars[i]['imageurl'])
            if "https:" not in topCars[i]['imageurl']:
                topCars[i]['imageurl'] = "https:" + topCars[i]['imageurl']
        print("\n5. The top 5 cars are returned to Chrome extension.\n")
        print("\nDone.\n")
        time8 = time.perf_counter()
        # print("Timer7 tempDataWrite:" + str(time8-time7))

        for i in range(len(topCars)):
            # print(topCars[i]['imageurl'])
            if "https:" not in topCars[i]['imageurl']:
                topCars[i]['imageurl'] = "https:" + topCars[i]['imageurl']
        print("\n5. The top 5 cars are returned to Chrome extension.\n")
        print("\nDone.\n")
    else:
        topCars = getPreferences(pricePriority, mileagePriority, yearPriority, 'NA', trimPriority)

    return topCars


#getPreferences(0,2,3,'NA',0)
# getCarData('hyundai', 'palisade','2022','22182',1,0,0,'NA',0)

app.run(host='0.0.0.0', port=8080)
