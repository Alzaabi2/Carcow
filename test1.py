from extension import *
from scrapeV1_6 import *
import json
import urllib
import requests
import random
import csv

def getMakeModel():
    filename = 'makemodel.json'
    carlist = []
    with open(filename) as f:
        # reader = csv.DictReader(f)
        # for row in reader:
        #     carlist.append(row)
        data = json.load(f)
        for i in data['results']:
            entry = {'Make': i['Make'], 'Model': i['Model'], 'Year':str(i['Year'])}
            carlist.append(entry)
            # print(entry)
    return carlist
    

def scrapeTest():
    print('Scrape Test 1 :')
    list = getMakeModel()
    r = random.random()
    r = round(r * 100)
    zip = 22201
    for i in list:
        # zip = zip + 300
        print(' ')
        print('Scraping: ['+i['Make']+', '+i['Model']+', '+i['Year']+', '+str(zip)+']')
        try:
            ScrapeAlpha(i['Make'], i['Model'], i['Year'], str(zip))
        except:
            print('Error')

    return


singleCar ={"Make": "Ford", "Model": "Challenger", "Year":"200"}

tempData = [{"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"},  {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": " 2,512 miles ", "Price": "$32,590 ", "VIN": "2C3CDZAG2NH140284", "url": "/used_cars/vehicle-detail/ul2152699317/dodge/challenger"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}]

with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        for i in range(len(tempData)):
            row = [tempData[i]['Make'], tempData[i]['Model'], tempData[i]['Year'], tempData[i]['Mileage'], tempData[i]['Price'], tempData[i]['VIN'], tempData[i]['url']]
            w.writerow(row)
            
        # f.write(json.dumps(singleCar))
        # f.write('\n')
        # for i in topCars:
        #     f.write(json.dumps(topCars))
        #     f.write(i)
        #     f.write('\n')



with open('TempData.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tempData.append(row)

print(tempData[3]['Year'])