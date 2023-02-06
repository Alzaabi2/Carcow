from ast import Continue
import csv
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import concurrent.futures
import itertools 
import json
from CarDepreciationValue import *
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

AWSPASSWORD = os.getenv('AWSPASSWORD')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)

carlist = []

def createList():
    csv_filename = 'cardata.csv'
    carlist =[]
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            carlist.append(row)
    
    return carlist

### rate function for LIVE scrape.
# This function takes in the actual price,
# the suggested price, and rates the car ###
def rate(list):
    deals = []
    if list is None:
        return []
    count = 1

    for i in range(len(list)):
        priceListed = list[i]['price']
        vin   = list[i]['VIN']

        mileage = list[i]['mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)

        suggested = dollarValueVin4(vin, miles[0])
        price = priceListed.replace(',', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')
        
        try:
            ratio = float(suggested)/float(price) #metric for rating deal
        except: 
            ratio == 'No Ratio'
 
        row = (str(count), vin,ratio,priceListed)
        count += 1
        deals.append(row)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: -y[2])

    topDeals = [deals[0], deals[1], deals[2], deals[3], deals[4]]
    return topDeals

### rate function that supports the implementation of the database
# i.e. we do not need this function for a LIVE scrape ###
def rate2(list):
    deals = []
    if list is None:
        return []
    count = 1

    for i in range(len(list)):
        price = list[i]['price']
        vin   = list[i]['VIN']

        price = price.replace(',', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')

        suggested = list[i]['suggested']
        if suggested == '0':
            continue

        try:
            ratio = float(price)/float(suggested) #metric for rating deal
        except: 
            ratio == 'No Ratio'

        url = list[i]['url']
        
        row = (str(count), vin,ratio,price,url)
        count += 1
        deals.append(row)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: y[2])

    ret_list = []

    # Ensure that all cars sent to Chrome extension are available
    print("\nAvailability validation:\n")
    for car in range(len(deals)):
        if len(ret_list) >= 5:
            break
        url = deals[car][4]
        available = True
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find('p', class_='sds-notification__desc') is not None:
            available = False
        elif soup.find('div', class_='text-bold text-size-600 text-size-sm-700 margin-vertical-7 margin-horizontal-7 text-center') is not None:
            if soup.find('div', class_='text-bold text-size-600 text-size-sm-700 margin-vertical-7 margin-horizontal-7 text-center').text == 'This car is no longer available. One moment while we take you to the search results page.':
                available = False
        elif soup.find('h2', class_='CVRsvD') is not None:
            available = False
        elif soup.find('h2', class_='pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0') is not None:
            if soup.find('h2', class_='pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0').text == 'Vehicle no longer available':
                available = False
        elif soup.find('div', class_='CDCXWUsedCarBuyPathExpiredListingHeaderText widget') is not None:
            available = False
        print("available = ", available,)
        if available == True:
            ret_list.append(deals[car])

    return ret_list


### Return top 5 cars with all the info from the database ###
def getTopCars(car_list, deals):
    topCars = []
    for n in range(len(deals)):
        found = False
        for c in car_list:
            if found == True:
                continue
            if(c['VIN'] == deals[n][1] and c['price'] == deals[n][3]):
                topCars.append(c)
                found = True
    return topCars

### Call Car Utils API with both VIN and mileage,
# and return the suggested value ###
def dollarValueVin4(vin, mileage):
    
    #duplicate check
    cursor = mydb.cursor(buffered=True,dictionary=True)
    cursor.execute("SELECT * FROM scraped WHERE VIN = %s;", (vin,))
    mydb.commit()
    
    list = cursor.fetchall()
    if len(list) != 0:
        return 'duplicate'
    
    url = "https://car-utils.p.rapidapi.com/marketvalue"

    querystring = {"vin": vin, "mileage": mileage}

    headers = {
        "X-RapidAPI-Key": "eabb27e940mshbaf991f2c492656p1afbb7jsnc31638e26d33",
        "X-RapidAPI-Host": "car-utils.p.rapidapi.com"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    apiResponse = response.text

    #if no market value data
    if '"vehicle":null' in response.text:
        return "0"
    while(1):
        if 'You have exceeded the rate limit per second for your plan, BASIC, by the API provider' in response.text:
            time.sleep(1)
            response = requests.request("GET", url, headers=headers, params=querystring)
            apiResponse = response.text
        else:
            break
    
    if '"message":"invalid vin"' in response.text:
        return '0'

    start = re.search('"prices":', response.text)
    end = re.search(',"distribution"', response.text)
    
    if start is None or end is None:
        return '0'
    if start.span() is None:
        return '0'
    listOfstart = start.span()
    if end.span() is None:
        return '0'
    listOfEnd   = end.span()
    start2      = listOfstart[1]
    end2        = listOfEnd[0]


    prices = apiResponse[start2 + 1:end2]

    avg  = re.search('"average":', prices)
    avg2 = avg.span()
    avgEnd = avg2[1]

    blw = re.search('"below":', prices)
    blw2   = blw.span()
    blwStart = blw2[0]
    blwEnd = blw2[1]
    

    abv = re.search('"above":', prices)
    abv2   = abv.span()
    abvStart = abv2[0]
    abvEnd = abv2[1]

    print("\n---------For VIN:", vin, " ---------")
    average = prices[avgEnd:blwStart - 1]
    print("AVERAGE:", average)

    below = prices[blwEnd:abvStart - 1]
    print("BELOW:", below)

    above = prices[abvEnd:]
    print("ABOVE:", above, "\n\n")
    time.sleep(1)
    return below