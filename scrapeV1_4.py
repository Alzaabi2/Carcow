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
import re


#This version of Scrape works on cars.com, it takes car specifications and outputs a csv file
# with the first 20 car search results. Each car will be described by Make,Model,Year,Mileage,Price.
# The scraping api used is BeautifulSoup



#Cars.com
def Scrape(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    
    url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=100&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    
    vins = ScrapeVin(make, model, year, zipcode)
    
    # search first 10 pages
    with open('cardata.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        # for n in range(1):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        cars = soup.find_all('div', class_="vehicle-card")
        # print(page.content)
    
        for c in cars:
            title = c.find('h2', class_="title").text
            # print(title)
            title = title.split(' ', 2)
            year = title[0]
            make = title[1]
            model = title[2]
            price = c.find('span', class_="primary-price").text
            carpage = 'http://cars.com' + c.find('a', class_="vehicle-card-link js-gallery-click-link").get('href')
            if not c.find('div', class_="mileage"):
                mileage = ' '#assume its brand new??
            else:
                mileage = c.find('div', class_="mileage").text
            
            vin = vins[vincount]    
            
            row = [make, model, year, mileage, price, vin, carpage]
            w.writerow(row)
            vincount+=1
            # url = getNextPage(soup)
            # if url == None:
            #     break

#Autotrader.com
def Scrape2(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    
    zipdata = json.loads(getZipData(zipcode))
    city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
    state = str(zipdata['results'][zipcode][0]['state_code'])

    # url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/'+city+'-'+state+'-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear='+year+'&endYear='+year+'&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    url = 'https://www.autotrader.com/cars-for-sale/all-cars/nissan/altima/newyork-ny-10003?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear=2014&endYear=2014&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    vins = ScrapeVin2(make, model, year, zipcode)
    
    # search first 10 pages
    with open('cardata2.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        # for n in range(1):
        page = requests.get(url, timeout=10000)
        soup = BeautifulSoup(page.content, 'html.parser') 
        # print(browser.page_source)
        cars = soup.find_all('div', class_="item-card-body margin-bottom-auto")
        # print(cars)
        for c in cars:
            if c == None:
                continue
            if c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled") == None:
                continue
            title = c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled").text
            print(title)
            title = title.split(' ')
            year = title[1]
            make = title[2]
            model = title[3]
            if c.find('span', class_="first-price") == None:
                continue
            price = c.find('span', class_="first-price").text
            carpage = 'https://www.autotrader.com' + c.find('a', rel="nofollow").get('href')
            if c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter"):
                mileageDivider = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter")
                if not mileageDivider.find('span', class_='text-bold'):
                    mileage = ' '#assume its brand new??
                else:
                    mileage = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold').text
            else:
                mileage = ' '
            vin = vins[vincount]    
            row = [make, model, year, mileage, price, vin, carpage]

            w.writerow(row)
            vincount+=1
            # url = getNextPage(soup)
            # if url == None:
            #     break

#cargurus.com
def Scrape3(make, model, year, zipcode):
    year = int(year)
    makesRequest = requests.get('https://www.cargurus.com/Cars/api/1.0/carselector/listMakes.action')
    makesList = json.loads(makesRequest.content)['makes']
    makeIDs = {}
    for n in makesList:
        name = n['name'].lower()
        makeIDs[name] = n['id']
    
    makeID = makeIDs[make.lower()]
    
    modelsRequest = requests.get('https://www.cargurus.com/Cars/api/1.0/carselector/listModels.action?searchType=USED&makeId='+makeID)
    modelsList = json.loads(modelsRequest.content)['models']
    modelIDs = {}
    for n in modelsList:
        name = n['name'].lower()
        modelIDs[name] = n['id']
        
    modelID = modelIDs[model.lower()]
    print(modelID)
    
    # minyear = soup.find('div', class_='HObdBl vT3i0_')
    # print(soup.encode("utf-8"))
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    url = 'https://www.cargurus.com/Cars/api/1.0/carselector/listingSearch.action?searchType=USED&entityId='+modelID+'&postalCode='+zipcode+'&distance=50'
    print(url)
    browser.get(url)
    minYear = browser.find_element(By.CSS_SELECTOR, "[aria-label='Select Minimum Year']")
    minYearInput = Select(minYear)
    minYeartext = year - 5
    # minYeartext = str(minYeartext)
    # minYearInput.select_by_visible_text(minYeartext)
    
    maxYear = browser.find_element(By.CSS_SELECTOR, "[aria-label='Select Maximum Year']")
    maxYearInput = Select(maxYear)
    #make sure year is not over current year
    maxYeartext = year + 5
    date = datetime.date.today()
    if maxYeartext > int(date.strftime("%Y")):
        maxYeartext = int(date.strftime("%Y")) + 1
    maxYeartext = str(maxYeartext)
    minYeartext = str(minYeartext)
    # print(browser.page_source.encode('utf-8'))
    time.sleep(2.5)#wait for year to update
    maxYearInput.select_by_visible_text(maxYeartext)
    minYearInput.select_by_visible_text(minYeartext)
    time.sleep(2.5)

    with open('cardata3.csv', 'w', encoding='utf8', newline='') as f:
        print(url)
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        for i in range(5):
            # if i == 0:
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            # else:
            #     page = requests.get(url)
            #     print("nexthtml:")
            #     soup = BeautifulSoup(page.content, 'html.parser')
            
            
            cars = soup.find_all('div', class_='soQyMy')
            if cars is not None:
                for c in cars:
                    # print(c.encode("utf-8"))
                    if c.find('h4', class_='vO42pn') == None:
                        continue
                    title = c.find('h4', class_='vO42pn').text
                    print(title)
                    title = title.split(' ', 3)
                    year = title[0]
                    make = title[1]
                    model = title[2]
                    trim = title[3]
                    print(trim)
                    if c.find('p', class_='JKzfU4 umcYBP').find('span', class_='') == None:
                        continue
                    mileage = c.find('p', class_='JKzfU4 umcYBP').find('span', class_='').text
                    print(mileage)
                    
                    #find vin index in dd list
                    extradata = c.find('dl', class_='O3A4fA').find_all('dt')
                    vinIndex = 0
                    for n in extradata:
                        if n.text == 'VIN':
                            break
                        vinIndex+1
                    
                    extradata2 = c.find('dl', class_='O3A4fA').find_all('dd') #contains vin
                    # if extradata == 
                    vin = extradata2[vinIndex-1].text
                    print(vin)
                    carpagepart = c.find('a', class_='lmXF4B c7jzqC A1f6zD').get('href')
                    carpage = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity='+modelID+'&distance=50&zip='+zipcode+'&sourceContext=carSelectorAPI' + carpagepart
                    price = c.find('span', class_='JzvPHo').text.split(' ', 1)
                    price = price[0]
                    print(price)
                    row = [make, model, year, mileage, price, vin, carpage]

                    w.writerow(row)
                # next page
            else:
                cars = soup.find_all('div', class_='contentWrap')
                for c in cars:
                    print(c.encode("utf-8"))
                    print(c.find('h4', class_='titleText').text)    
                
            url = 'https://www.cargurus.com/Cars/api/1.0/carselector/listingSearch.action?searchType=USED&entityId='+modelID+'&postalCode='+zipcode+'&distance=50&sourceContext=carSelectorAPI#resultsPage=' + str(i+2)
            time.sleep(5)
            print(url)
                
    

#cars.com 
def getNextPage(soup):
    page = soup.find('div', class_='sds-pagination__controls')
    next = page.find('button', id="next_paginate")
    if next == None: 
        next = page.find('a', id="next_paginate")
    url = 'http://cars.com' + str(next.get('href'))
    if url == 'http://cars.comNone':
        print('no next page')
        return
    return url


      
#cars.com  
def ScrapeVin(make,model,year,zipcode):
    make = make.lower()
    model = model.lower()
    url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=100&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    
    with open('carvins.csv', 'w', encoding='utf8', newline='') as f:
        vins = []
        for n in range(10):
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser') 
            searchContent = soup.find('div', class_="sds-page-section listings-page").get('data-site-activity')
            seperator = searchContent.split(',')
            for c in seperator:
                seperator2 = c.split(':')
                
                if(seperator2[0] == '"vin"'):
                    vin = seperator2[1].replace('"', '')
                    f.write(str(vin))
                    f.write('\n')
                    vins.append(str(vin))
            url = getNextPage(soup)
            if url == None:
                break
                
    return vins

#autotrader.com
def ScrapeVin2(make,model,year,zipcode):
    make = make.lower()
    model = model.lower()
    
    zipdata = json.loads(getZipData(zipcode))
    city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
    state = str(zipdata['results'][zipcode][0]['state_code'])

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/'+city+'-'+state+'-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear='+year+'&endYear='+year+'&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    print(url)
    with open('carvins2.csv', 'w', encoding='utf8', newline='') as f:
        vins = []
        # for n in range(1):
        page = requests.get(url, timeout=10000)
        soup = BeautifulSoup(page.content, 'html.parser') 
        searchContent = soup.find_all('script')
        for n in searchContent:
            if 'vehicleIdentificationNumber' in n.text:
                j = json.loads(n.text)
                vins.append(j['vehicleIdentificationNumber'])
                f.write(j['vehicleIdentificationNumber'])
                f.write('\n')
                
            # if not 'vehicleIdentificationNumber' in n.text:
            #     searchContent.remove(n)
        
        # print(searchContent)
        # seperator = searchContent.split(',')
        
    #     for c in seperator:
    #         seperator2 = c.split(':')
            
    #         if(seperator2[0] == '"vehicleIdentificationNumber"'):
    #             vin = seperator2[1].replace('"', '')
    #             f.write(str(vin))
    #             f.write('\n')
    #             vins.append(str(vin))
    #         # url = getNextPage(soup)
    #         # if url == None:
    #         #     break
                
    return vins
    
        
def ScrapeToList(make, model, year, zipcode):
    make = make.lower()
    model = model.lower()
    url = 'https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D=' + make + '&models%5B%5D=' + make + '-' + model +'&list_price_max=&maximum_distance=20&zip=' + zipcode
    url2 = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=20&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    page = requests.get(url2)
    soup = BeautifulSoup(page.content, 'html.parser')
    cars = soup.find_all('div', class_="vehicle-card")
    ret_list = []
    for c in cars:
        title = c.find('h2', class_="title").text
        title = title.split(' ', 2)
        year = title[0]
        make = title[1]
        model = title[2]
        price = c.find('span', class_="primary-price").text
        mileage = c.find('div', class_="mileage").text
        row = [make, model, year, mileage, price]
        ret_list.append(row)
    return ret_list


### This function will find the MSRP of each different trim of the specified car ###
# Working
def scrapeTrimPrice(make, model, year, trim):
    url = 'https://www.cars.com/research/audi-a3-2018/specs/'
    
#get data from ZIP    
def getZipData(zipcode):
    apikey = "84f30620-5c5d-11ed-a2ab-01db54110476"
    response = requests.get('https://app.zipcodebase.com/api/v1/search?apikey='+apikey+'&country=US&codes='+zipcode)
    return response.text



# Scrape3('Jeep', 'Wrangler', '2020', '22043')
<<<<<<< HEAD
Scrape3('Nissan', 'Altima', '2014', '10003')
=======
# Scrape3('Nissan', 'Altima', '2014', '10003')
>>>>>>> e2600f3e4d9c0d5b6985d1bcb4c740adba5b7e0e
