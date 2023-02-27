import string
from bs4 import BeautifulSoup
import requests
from csv import writer
import json
import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import *
from dotenv import load_dotenv
from iteration_utilities import unique_everseen

load_dotenv()

AWSPASSWORD = os.getenv('AWSPASSWORD')

mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password= AWSPASSWORD,
    database="CarCowDB"
)


#This function scrapes the input url for all the cars listed in that page sequence and returns a list of dictionaries
#Input: 
#   url
#   HTMLclass - class text in the html tag for a car listing item
#   HTMLitem - the name of the tag
#example: url = https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=jeep&models%5B%5D=&list_price_max=&maximum_distance=30&zip=22101
#         HTMLclass = vehicle-card
#         HTMLitem = div
def DynamicScrape(url,HTMLclass, HTMLitem):
    
    #get makes and models from database:
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT Distinct make, model, trim, year FROM tbl_models")
    databaseList = cursor.fetchall()
    cursor.execute("SELECT Distinct make FROM tbl_models")
    makes = cursor.fetchall()
    cursor.execute("SELECT Distinct make, model FROM tbl_models")
    models = cursor.fetchall()
    cursor.execute("SELECT Distinct make, model, trim FROM tbl_models")
    trims = cursor.fetchall()
    
    for n in models:
        if n['make'] == 'jeep':
            print(n)
    
    print(len(makes))
    print(len(models))
    print(len(trims))
    print(len(databaseList))
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cars = soup.find_all(HTMLitem , class_=HTMLclass)
    
    counter = 0
    for c in cars:
        counter += 1 
        print('car #'+str(counter))
        makeCountList = {}
        carFound = False
        regex = r'\b(19|20)\d{2}\b'
        # url = 
        for m in models:
        #     for i in c.text.split('\n'):
        #         matched = False
        #         match = re.match(regex, i)
        #         #if make and model are found in database
        #         if ((m['make'].replace('_', ' ').capitalize() in i) and (m['model'].replace('_', ' ').capitalize() in i) and match) or ((m['make'].replace('_', ' ').lower() in i) and (m['model'].replace('_', ' ').lower() in i) and match) or ((m['make'].replace('_', ' ').upper() in i) and (m['model'].replace('_', ' ').upper() in i) and match):
        #             # if m not in makeCountList.keys():
        #             #     makeCountList[m] = 0
        #             # makeCountList[m] += 1
        #             print(m)
        #             matched = True
        #             carFound = True
        #         elif((m['make'].replace('_', ' ').capitalize() in i) and match and not carFound
        #             ) or (
        #             (m['make'].replace('_', ' ').lower() in i) and match and not carFound
        #             ) or (
        #             (m['make'].replace('_', ' ').upper() in i) and match and not carFound):
        #             # if m not in makeCountList.keys():
        #         #     #     makeCountList[m] = 0
        #         #     # makeCountList[m] += 1
        #             m1 = i.split(m['make'].replace('_', ' ').capitalize())
        #             if m1[0] == i:
        #                 m1 = i.split(m['make'].replace('_', ' ').lower())
        #             if m1[0] == i: 
        #                 m1 = i.split(m['make'].replace('_', ' ').upper())
        #             # print("m1")
        #             # print(m1)
        #             m2 = m1[1].split(' ')
        #             m3 = m2[0]
        #             # print('m3')
        #             # print(m3)
        #             # print(m)
        #             matched = True
        #             # carFound = True
        #             print('considering '+m['make']+' in '+i)
        # if not carFound: 
        #     print('not found') 
            for i in c:
                print(i)
        print('----------------------')                
                
                
                
        # make = None
        # makeCounter = 0
        # for k,v in makeCountList.items():
        #     if make is None:
        #         make = k
        #         makeCounter = v
        #         continue
        #     if v > makeCounter:
        #         make = k
        #         makeCounter = v
        # print("    "+make)
            
        

DynamicScrape('https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=jeep&models%5B%5D=&list_price_max=&maximum_distance=30&zip=22101', 'vehicle-card', 'div')