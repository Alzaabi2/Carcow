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
import difflib

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
    
    cursor.execute("SELECT Distinct make, model, trim FROM tbl_models")
    trims = cursor.fetchall()
    
    saved_queries = {}
    
    # for n in models:
    #     if n['make'] == 'jeep':
    #         print(n)
    
    # print(len(makes))
    # print(len(models))
    # print(len(trims))
    # print(len(databaseList))
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cars = soup.find_all(HTMLitem , class_=HTMLclass)
    
    counter = 0
    for c in cars:
        counter += 1 
        print('car #'+str(counter))
        makeCountList = {}
        carFound = False
        make_match = None
        regex = r'\b(19|20)\d{2}\b'
        model_match = None
        trim_match = None
        isNew = False
        mileage_match = None
        # url = 
        for m in makes:
            for i in c.text.split('\n'):
                
                year_regex = re.match(regex, i)
                #find make with in the text
                if((m['make'].replace('_', ' ').capitalize() in i) and year_regex
                    ) or (
                    (m['make'].replace('_', ' ').lower() in i) and year_regex
                    ) or (
                    (m['make'].replace('_', ' ').upper() in i) and year_regex):
                    # if m not in makeCountList.keys():
                #     #     makeCountList[m] = 0
                #     # makeCountList[m] += 1
                
                    # m1 = i.split(m['make'].replace('_', ' ').capitalize())
                    # if m1[0] == i:
                    #     m1 = i.split(m['make'].replace('_', ' ').lower())
                    # if m1[0] == i: 
                    #     m1 = i.split(m['make'].replace('_', ' ').upper())
                    # # print("m1")
                    # # print(m1)
                    # m2 = m1[1].split(' ')
                    # m3 = m2[0]
                    
                    # print('m3')
                    # print(m3)
                    # print(m)
                    year_match = year_regex.group(0)
                    make_match = m['make'].capitalize()
                    # carFound = True
        if make_match is None: 
            print('make not found')
        else:
            #now search for model in the text
            query = 'SELECT Distinct make, model FROM tbl_models WHERE make = "'+make_match+'"'
            # print(query)
            #check if query was saved from last search
            if query not in saved_queries.keys(): 
                cursor.execute(query)
                models = cursor.fetchall()
            else:
                models = saved_queries[query]
                # print('found saved query: '+str(len(models)))
            
            
            # if len(models) == 0:
            #     alt_query = 'SELECT Distinct make, model FROM tbl_models WHERE make = "'+make_match+'" AND year = "'+str(int(year_match)-1)+'"'
            #     cursor.execute(alt_query)
            #     models = cursor.fetchall()
                
            saved_queries[query] = models
                        
            #search for the format Year Make Model
            key_phrase = year_match + ' ' + make_match
            possible_models = []
            for i in c.text.split('\n'):
                if key_phrase in i:
                    model_phrase = i.replace(key_phrase, '')
                    # print('model phrase: ' + model_phrase)
                    #find closest match to model
                    model_match = difflib.get_close_matches(model_phrase, [mo['model'] for mo in models],cutoff=0)[0]
                # for mo in models:
                #     if((mo['model'].replace('_', ' ').capitalize() in i) and (key_phrase in i)
                #         ) or (
                #         (mo['model'].replace('_', ' ').lower() in i) and (key_phrase in i)
                #         ) or (
                #         (mo['model'].replace('_', ' ').upper() in i) and (key_phrase in i)):
                #         model_match = mo['model'].capitalize()
                #         print('considering model '+year_match+" "+make_match+" "+model_match)
            # print(model_match)
            if model_match is None: 
                print('model not found')
                #the case where the model is not stored in the database
                for i in c.text.split('\n'):
                    if key_phrase in i:
                        matched_phrase = i.split(key_phrase)
                        #get the first word after the key phrase
                        model_match = matched_phrase[1].split(' ')[1]
                        print(model_match)
                        query = 'INSERT INTO tbl_models (make, model, year) VALUES ("'+make_match+'","'+model_match+'","'+year_match+'")'
                        print(query)
                        cursor.execute(query)  
                        mydb.commit()             
            
            #find list of trims
            query = 'SELECT Distinct make, model, trim FROM tbl_models WHERE make = "'+make_match+'" AND model = "'+model_match+'"'
            #check if query was saved from last search
            if query not in saved_queries.keys(): 
                cursor.execute(query)
                trims = cursor.fetchall()
            else:
                trims = saved_queries[query]
            key_phrase = year_match + ' ' + make_match + ' ' + model_match
            #check matching trim and mileage regex
            regex = r'\d{1,3}(,\d{3})*\s*(mi|miles|mi.?)'
            for i in c.text.split('\n'):
                #make sure mileage is taken, not distance
                if 'away' not in i or 'from' not in i:
                    mileage_regex = re.match(regex, i)
                    if mileage_regex:
                        mileage_match = mileage_regex.group(0)
                #check for keyword new:
                if 'New' in i:
                    isNew = True
                #find closest trim matching the car description
                if key_phrase in i:
                    trim_phrase = i.replace(key_phrase, '').replace('used', '').replace('USED', '').replace('Used', '').replace('new', '').replace('NEW', '').replace('New', '')
                    # print('trim phrase' + trim_phrase)
                    trim_match = difflib.get_close_matches(trim_phrase, [t['trim'] for t in trims], cutoff=0)
                    if len(trim_match) > 0:
                        trim_match = trim_match[0]
                    else:
                        trim_match = ''
            if trim_match is None:
                trim_match = ''
            if mileage_match is None and isNew is True:
                mileage_match = 0
            print(mileage_match)
        print(''+year_match+" "+make_match+" "+model_match+" "+trim_match)
            
          
            # for i in c:
        # print(c.text)
        
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