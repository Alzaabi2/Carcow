from extension import *
from scrapeV1_6 import *
import json
import urllib
import requests
import random

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


scrapeTest()