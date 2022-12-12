####
# V1.7
# Scrape with threading
# incomplete
###


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

#This version of Scrape works on cars.com, it takes car specifications and outputs a csv file
# with the first 20 car search results. Each car will be described by Make,Model,Year,Mileage,Price.
# The scraping api used is BeautifulSoup

vins1 = []
    
scrapedList1 = []

vincount1 = 0

#Cars.com
def Scrape1(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    
    url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=100&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    
    global vins1 
    vins1 = ScrapeVin(make, model, year, zipcode)
    
    global scrapedList1 
    scrapedList1 = []
    
    global vincount1
    vincount1 = 0
    
    # search first 10 pages
    with open('cardata.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        cars = soup.find_all('div', class_="vehicle-card")
        print(str(len(cars)))
        with ThreadPoolExecutor() as executor:
            executor.map(Scrape1Loop,cars)
        
    print('Scraped '+str(len(scrapedList1))+' cars from Cars.com')
    return scrapedList1

def Scrape1Loop(c):
        global vincount1
        global scrapedList1
        global vins1

        if not c.find('h2', class_="title"):
            return
        title = c.find('h2', class_="title").text
        title = title.split(' ', 2)
        year = title[0]
        make = title[1]
        model = title[2]
        
        if not c.find('span', class_="primary-price"):
            return
        price = c.find('span', class_="primary-price").text
        
        if not c.find('a', class_="vehicle-card-link js-gallery-click-link"):
            return
        carpage = 'http://cars.com' + c.find('a', class_="vehicle-card-link js-gallery-click-link").get('href')
        
        if not c.find('div', class_="mileage"):
            mileage = ' '#assume its brand new??
        else:
            mileage = c.find('div', class_="mileage").text
        
        vin = vins1[vincount1]    
        
        row = [make, model, year, mileage, price, vin, carpage]
        rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
        # w.writerow(row)
        scrapedList1.append(rowlist)
        vincount1+=1
    
    


#Autotrader.com
def Scrape2(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    
    zipdata = json.loads(getZipData(zipcode))
    city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
    state = str(zipdata['results'][zipcode][0]['state_code'])

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/'+city+'-'+state+'-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear='+year+'&endYear='+year+'&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    vins = ScrapeVin2(make, model, year, zipcode)
    scrapedList = []
    # search first 10 pages
    with open('cardata2.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        page = requests.get(url, timeout=10000)
        soup = BeautifulSoup(page.content, 'html.parser') 
        cars = soup.find_all('div', class_="item-card-body margin-bottom-auto")
        for c in cars:
            if c == None:
                continue
            if c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled") == None:
                continue
            title = c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled").text
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
            rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
            w.writerow(row)
            scrapedList.append(rowlist)
            vincount+=1
    print('Scraped '+str(len(scrapedList))+' cars from autotrader.com')
    return scrapedList



#cargurus.com
def Scrape3(make, model, year, zipcode):
    scrapedList = []
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
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    url = 'https://www.cargurus.com/Cars/api/1.0/carselector/listingSearch.action?searchType=USED&entityId='+modelID+'&postalCode='+zipcode+'&distance=50'
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
    
    time.sleep(2.5)#wait for year to update
    try:
        maxYearInput.select_by_visible_text(maxYeartext)
    except: 
        if maxYeartext == '2023':
            maxYeartext = '2022'
        maxYearInput.select_by_visible_text(maxYeartext)
    minYearInput.select_by_visible_text(minYeartext)
    time.sleep(2.5)

    with open('cardata3.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        for i in range(5):
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            
            cars = soup.find_all('div', class_='soQyMy')
            if cars is not None:
                for c in cars:
                    if c.find('h4', class_='vO42pn') == None:
                        continue
                    title = c.find('h4', class_='vO42pn').text
                    title = title.split(' ', 3)
                    year = title[0]
                    make = title[1]
                    model = title[2]
                    trim = title[3]
                    if c.find('p', class_='JKzfU4 umcYBP').find('span', class_='') == None:
                        continue
                    mileage = c.find('p', class_='JKzfU4 umcYBP').find('span', class_='').text
                    
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
                    carpagepart = c.find('a', class_='lmXF4B c7jzqC A1f6zD').get('href')
                    carpage = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity='+modelID+'&distance=50&zip='+zipcode+'&sourceContext=carSelectorAPI' + carpagepart
                    price = c.find('span', class_='JzvPHo').text.split(' ', 1)
                    price = price[0]
                    
                    row = [make, model, year, mileage, price, vin, carpage]
                    rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
                    w.writerow(row)
                    scrapedList.append(rowlist)

                # next page
                
            url = 'https://www.cargurus.com/Cars/api/1.0/carselector/listingSearch.action?searchType=USED&entityId='+modelID+'&postalCode='+zipcode+'&distance=50&sourceContext=carSelectorAPI#resultsPage=' + str(i+2)
            time.sleep(5)    
    print('Scraped '+str(len(scrapedList))+' cars from cargurus.com')    
    return scrapedList


#edmunds.com
def Scrape4(make, model, year, zipcode):
    scrapedList = []

    make = make.lower()
    model = model.lower()
    
    minyear = str(int(year) - 5)
    maxyear = str(int(year) + 5)
    
    url = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used&make='+make+'&model='+model+'&radius=50&year='+minyear+'-'+maxyear+''
    # search first 10 pages
    with open('cardata4.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        # header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        for n in range(5):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            cars = soup.find_all('div', class_="d-flex flex-column usurp-inventory-card w-100 srp-expanded")
                
            for c in cars:
                if c.find('span', class_="size-24 font-weight-bold text-gray-darker") == None:
                    continue
                price = c.find('span', class_="size-24 font-weight-bold text-gray-darker").text
                if c.find('div', class_='size-16 font-weight-bold mb-0_5 text-primary-darker') == None:
                    continue
                title = c.find('div', class_='size-16 font-weight-bold mb-0_5 text-primary-darker').text
                if c.find('div', class_='font-weight-normal size-14 text-gray-dark') == None:
                    continue
                trim = c.find('div', class_='font-weight-normal size-14 text-gray-dark').text
                if c.find('span', class_='icon-meter text-gray-darker key-point-icon d-inline-block size-12 mr-0_5') == None:
                    continue
                mileage = c.find('span', class_='').text
                title = title.split(' ')
                year = title[0]
                make = title[1]
                model = title[2]
                
                link = c.find('a', class_='usurp-inventory-card-vdp-link').get('href')
                carpage = 'https://www.edmunds.com'+link
                parseLink = link.split('/')
                vin = parseLink[5]

                # row = [make, model, trim, year, mileage, price, vin, carpage]
                row = [make, model, year, mileage, price, vin, carpage]
                rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
                w.writerow(row)
                scrapedList.append(rowlist)
            url = getNextPage4(soup)
            if url == None:
                break
    print('Scraped '+str(len(scrapedList))+' cars from edmunds.com')
    return scrapedList

#carsdirect.com
def Scrape5(make, model, year, zipcode):
    scrapedList = []
    make = make.lower()
    model = model.lower()
    
    minyear = str(int(year) - 5)
    maxyear = str(int(year) + 5)
    
    url = 'https://www.carsdirect.com/used_cars/listings/' + make + '/' + model + '?zipcode=' + zipcode + '&dealerId=&distance=&yearFrom=' + minyear + '&yearTo=' + maxyear + '&priceFrom=&priceTo=&qString=' + make + '%603%6020%600%600%60false%7C' + model + '%604%60380%600%600%60false%7C&keywords=&makeName=' + make + '&modelName=' + model + '&sortColumn=&sortDirection=&searchGroupId=&lnk='
    # search first 3 pages
    with open('cardata5.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        # header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        for n in range(3):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            cars = soup.find_all('div', class_="list-row")
            for c in cars:
                title = c.find('span', class_='listing-header').text
                title = title.split(' ')
                year = title[0]
                make = title[1]
                model = title[2]
                if c.find('a', class_='detail-price').find('span') is None:
                    continue
                price = c.find('a', class_='detail-price').find('span').text
                if c.find('div', class_="mileage").find('span') is None:
                    continue
                mileage = c.find('div', class_="mileage").find('span').text
                if c.find('span', class_='trimspan') is None:
                    continue
                trim = c.find('span', class_='trimspan').text
                if c.find('span', class_='WrapperButtonSave') is None:
                    continue
                vin = c.find('span', class_='WrapperButtonSave').get('vin')
                if c.find('meta') is None:
                    continue
                carpage = c.find('meta').get('content')
                url = 'https://www.carsdirect.com' + carpage
                
                # row = [make, model, trim, year, mileage, price, vin, url]
                row = [make, model, year, mileage, price, vin, carpage]
                rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
                w.writerow(row)
                scrapedList.append(rowlist)
            url = getNextPage5(soup)
            if url == None:
                break 
    print('Scraped '+str(len(scrapedList))+' cars from carsdirect.com')
    return scrapedList

#cars.com       
def getNextPage(soup):
    if soup is None:
        return None
    page = soup.find('div', class_='sds-pagination__controls')
    next = page.find('button', id="next_paginate")
    if next == None: 
        next = page.find('a', id="next_paginate")
    url = 'http://cars.com' + str(next.get('href'))
    if url == 'http://cars.comNone':
        # print('no next page')
        return
    return url

#edmunds.com
def getNextPage4(soup):
    if soup is None:
        return None
    next = soup.find('a', class_="pagination-btn rounded d-flex align-items-center justify-content-center text-primary-darker mx-1_5")

    url = 'http://www.edmunds.com' + str(next.get('href'))
    if url == 'http://www.edmunds.comNone':
        # print('no next page')
        return None
    return url

#carsdirect.com
def getNextPage5(soup):
    if soup is None:
        return None
    allLinks = soup.find_all('a', class_="pagerLink")
    next = None
    for l in allLinks:
        if l.find('span', class_="icon-chevron-right") is not None:
            next = l
    
    if next == None:
        return None
       
    url = 'http://www.carsdirect.com' + str(next.get('href'))
    if url == 'http://www.carsdirect.comNone':
        # print('no next page')
        return None
    return url
      
#cars.com  
def ScrapeVin(make,model,year,zipcode):
    make = make.lower()
    model = model.lower()
    url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=100&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    
    with open('carvins.csv', 'w', encoding='utf8', newline='') as f:
        vins = []
        # for n in range(10):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser') 
        searchContent = soup.find('div', class_="sds-page-section listings-page").get('data-site-activity')
        seperator = searchContent.split(',')
        with ThreadPoolExecutor() as executor:
            executor.map(scrapeVinLoop,seperator)           
            # url = getNextPage(soup)
            # if url == None:
            #     break         
    return vins1

def scrapeVinLoop(c):
    global vins1
    
    seperator2 = c.split(':')      
    if(seperator2[0] == '"vin"'):
        vin = seperator2[1].replace('"', '')
        vins1.append(str(vin))

#autotrader.com
def ScrapeVin2(make,model,year,zipcode):
    make = make.lower()
    model = model.lower()
    
    zipdata = json.loads(getZipData(zipcode))
    city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
    state = str(zipdata['results'][zipcode][0]['state_code'])

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/'+city+'-'+state+'-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear='+year+'&endYear='+year+'&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
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


#incomplete
### This function will find the MSRP of each different trim of the specified car ###
# Working
def scrapeTrimPrice(make, model, year, trim):
    url = 'https://www.cars.com/research/audi-a3-2018/specs/'
    
    
#get data from ZIP    
def getZipData(zipcode):
    apikey = "84f30620-5c5d-11ed-a2ab-01db54110476"
    response = requests.get('https://app.zipcodebase.com/api/v1/search?apikey='+apikey+'&country=US&codes='+zipcode)
    return response.text

from concurrent.futures import ThreadPoolExecutor

def ScrapeAlpha(make, model, year, zipcode):

    with ThreadPoolExecutor() as executor:
        try:
            executor.submit(Scrape1(make, model, year, zipcode))
        except:
            "Scrape1 failed"
            l1 = []
        try:
            l2 = Scrape2(make, model, year, zipcode)
        except:
            "Scrape2 failed"
            l2 = []
        try:
            l3 = Scrape3(make, model, year, zipcode)
        except:
            "Scrape3 failed"
            l3 = []
        try:
            l4 = Scrape4(make, model, year, zipcode)
        except:
            "Scrape4 failed"
            l4 = []
        try:
            l5 = Scrape5(make, model, year, zipcode)
        except:
            "Scrape5 failed"
            l5 = []
    
    scrapedList = l1 + l2 + l3 + l4 + l5
    # for c in scrapedList:
    #     print(scrapedList)
    print('length = [' + str(len(l1)) + ' + ' + str(len(l2)) + ' + ' + str(len(l3)) + ' + '+ str(len(l4)) + ' + '+ str(len(l5)) + '] = ' + str(len(scrapedList)))
    return scrapedList


def ScrapeAlpha(make, model, year, zipcode):

    with ThreadPoolExecutor() as executor:
        try:
            f1 = executor.submit(Scrape1(make, model, year, zipcode))
            l1 = f1.result()
        except:
            "Scrape1 failed"
            l1 = []
        try:
            f2 = executor.submit(Scrape2(make, model, year, zipcode))
            l2 = f2.result()
        except:
            "Scrape2 failed"
            l2 = []
        try:
            f3 = executor.submit(Scrape3(make, model, year, zipcode))
            l3 = f3.result()
        except:
            "Scrape3 failed"
            l3 = []
        try:
            f4 = executor.submit(Scrape4(make, model, year, zipcode))
            l4 = f4.result()
        except:
            "Scrape4 failed"
            l4 = []
        try:
            f5 = executor.submit(Scrape5(make, model, year, zipcode))
            l5 = f5.result()
        except:
            "Scrape5 failed"
            l5 = []
    
    scrapedList = l1 + l2 + l3 + l4 + l5
    # for c in scrapedList:
    #     print(scrapedList)
    print('length = [' + str(len(l1)) + ' + ' + str(len(l2)) + ' + ' + str(len(l3)) + ' + '+ str(len(l4)) + ' + '+ str(len(l5)) + '] = ' + str(len(scrapedList)))
    return scrapedList


def ScrapeAlpha2(make, model, year, zipcode):
    
    
    try:
        l1 = Scrape1(make, model, year, zipcode)
    except:
        "Scrape1 failed"
        l1 = []
    time2 = time.perf_counter()
    try:
        l2 = Scrape2(make, model, year, zipcode)
    except:
        "Scrape2 failed"
        l2 = []
    time3 = time.perf_counter()
    print("scrape2:" + str(time3-time2))
    try:
        l3 = Scrape3(make, model, year, zipcode)
    except:
        "Scrape3 failed"
        l3 = []
    time4 = time.perf_counter()
    print("scrape3:" + str(time4-time3))
    try:
        l4 = Scrape4(make, model, year, zipcode)
    except:
        "Scrape4 failed"
        l4 = []
    time5 = time.perf_counter()
    print("scrape4:" + str(time5-time4))
    try:
        l5 = Scrape5(make, model, year, zipcode)
    except:
        "Scrape5 failed"
        l5 = []
    time6 = time.perf_counter()
    print("scrape5:" + str(time6-time5))
        
    scrapedList = l1 + l2 + l3 + l4 + l5
    # for c in scrapedList:
    #     print(scrapedList)
    print('length = [' + str(len(l1)) + ' + ' + str(len(l2)) + ' + ' + str(len(l3)) + ' + '+ str(len(l4)) + ' + '+ str(len(l5)) + '] = ' + str(len(scrapedList)))
    return scrapedList


#removes duplicate data
def cleanData(list):
    print(list)
    print('results list')
    res_list = []
    for i in range(len(list)):
        if list[i] not in list[i + 1:]:
            res_list.append(list[i])
            
    return res_list      
    
    

# time1 = time.perf_counter()
# ScrapeAlpha('Nissan', 'Altima', '2014', '10003')
# Scrape1('Nissan', 'Altima', '2021', '22201')

# time2 = time.perf_counter()
# print("timer Threads:" + str(time2-time1))
# ScrapeAlpha2('Nissan', 'Altima', '2014', '10003')
# time3 = time.perf_counter()
# print("timer regular:" + str(time3-time2))
