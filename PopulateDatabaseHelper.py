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
from lxml import etree
from scrapeV1_6_database_mass_search import *
from database import *

def getMakes():
    page = requests.get('https://www.cars.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    makesPathList = soup.find_all('select', class_='sds-text-field')
    for i in makesPathList:
        if i.get('id') == 'makes':
            makesPath = i
    makesPath2 = makesPath.find_all('option')
    makesList = []
    for i in makesPath2:
        makesList.append(i.text)
    makesList.remove('All makes')
    # print(makesList)
    return makesList

def getModels():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    url = 'https://www.cars.com/'
    browser.get(url)
    
    browser.find_element(By.XPATH, '/html/body/section/div[2]/div[1]/section[2]/div[1]/div/div/form[1]/div/div/div[1]/div/select/option[4]').click()
        
    makesList = getMakes()
    modelsList = []
    counter = 1
    group = 1
    for n in makesList:
        if n == 'AC':
            counter = 1
            group = 2
        print('group = '+str(group)+'counter = '+str(counter))
        try:
            makesSelect = browser.find_element(By.XPATH, '/html/body/section/div[2]/div[1]/section[2]/div[1]/div/div/form[1]/div/div/div[2]/div/select/optgroup['+str(group)+']/option['+str(counter)+']').click()
        except:
            print('Not Found: '+'group = '+str(group)+'counter = '+str(counter))
        # makesInput = Select(makesSelect)
        # makesInput.select_by_visible_text(n)
        time.sleep(4)
        counter+=1
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        modelsPathList = soup.find_all('select', class_='sds-text-field')
        for i in modelsPathList:
            if i.get('id') == 'models':
                modelsPath = i
        modelsPath2 = modelsPath.find_all('option')
        for i in modelsPath2:
            modelsList.append([n,i.text])
        # except:
        #     print(n+' not found')
    
    # print(modelsList) 
    return modelsList
    
def massScrape1():
    modelsList = getModels()
    makesList = getMakes()
    errorList = []
    for i in makesList:
        try:
            scrapedData = Scrape1(i)
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape1 Error: '+i)
    print(errorList)

def massScrape2():
    modelsList = getModels()
    makesList = getMakes()
    errorList = []
    for i in modelsList:
        try:
            scrapedData = Scrape2(i[0],i[1])
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape2 Error: '+i)
    print(errorList)
            
def massScrape3():
    modelsList = getModels()
    makesList = getMakes()
    errorList = []
    for i in makesList:
        try:
            scrapedData = Scrape3(i)
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape3 Error: '+i)            
    print(errorList)    
    
def massScrape4():
    modelsList = getModels()
    makesList = getMakes()
    errorList = []
    for i in modelsList:
        try:
            scrapedData = Scrape4(i[0],i[1])
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape4 Error: '+i)
    print(errorList)
    
def massScrape5():
    modelsList = getModels()
    makesList = getMakes()
    errorList = []
    for i in modelsList:
        try:
            scrapedData = Scrape5(i[0],i[1])
            populateScraped(scrapedData)
            print('Completed '+i)
        except:
            errorList.append('Scrape5 Error: '+i)
    print(errorList)
              
# getModels()
massScrape4()