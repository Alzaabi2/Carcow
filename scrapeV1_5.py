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
#zipcode not considered 
def Scrape2(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    minYear = (str(int(year)- 5))
    maxYear = (str(int(year)+ 5))
    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'woodbridge-va-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear='+minYear+'&endYear='+maxYear+'&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    vins = ScrapeVin2(make, model, year, zipcode)
    
    # search first 10 pages
    with open('cardata2.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        # for n in range(1):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        cars = soup.find_all('div', class_="item-card-body margin-bottom-auto")
    
        for c in cars:
            title = c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled").text
            # print(title)
            title = title.split(' ')
            year = title[1]
            make = title[2]
            model = title[3]
            price = c.find('span', class_="first-price").text
            carpage = 'https://www.autotrader.com' + c.find('a', rel="nofollow").get('href')
            if not c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold'):
                mileage = ' '#assume its brand new??
            else:
                mileage = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold').text
            
            vin = vins[vincount]    
            row = [make, model, year, mileage, price, vin, carpage]

            w.writerow(row)
            vincount+=1
            # url = getNextPage(soup)
            # if url == None:
            #     break

#not working
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
    browser.get(url)
    minYear = browser.find_element(By.CSS_SELECTOR, "[aria-label='Select Minimum Year']")
    minYearInput = Select(minYear)
    minYeartext = year - 5
    minYeartext = str(minYeartext)
    # minYearInput.select_by_visible_text(minYeartext)
    
    maxYear =  WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Select Maximum Year']")))
    maxYearInput = Select(maxYear)
    #make sure year is not over current year
    maxYeartext = year + 5
    date = datetime.date.today()
    if maxYeartext > int(date.strftime("%Y")):
        maxYeartext = int(date.strftime("%Y"))
    minYeartext = str(minYeartext)
    print('type2 '+type(minYeartext))
    # maxYearInput.select_by_visible_text(maxYeartext)
    # print(browser.page_source.encode('utf-8'))
    time.sleep(2.5)#wait for year to update
    
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    cars = soup.find_all('div', class_='bkPbpj R5t9rZ')
    for c in cars:
        title = c.find('h4', class_='vO42pn').text
        print(title)
    

    
    # make = make.lower()
    # model = model.lower()
    
    # url = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d894&zip=22191'
    # url = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=22191&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=d896'
    # vins = ScrapeVin2(make, model, year, zipcode)
    
    # # search first 10 pages
    # with open('cardata2.csv', 'w', encoding='utf8', newline='') as f:
    #     w = writer(f)
    #     header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
    #     w.writerow(header)
    #     vincount = 0
    #     # for n in range(1):
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     cars = soup.find_all('div', class_="item-card-body margin-bottom-auto")
    
    #     for c in cars:
    #         title = c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled").text
    #         # print(title)
    #         title = title.split(' ')
    #         year = title[1]
    #         make = title[2]
    #         model = title[3]
    #         price = c.find('span', class_="first-price").text
    #         carpage = 'https://www.autotrader.com' + c.find('a', rel="nofollow").get('href')
    #         if not c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold'):
    #             mileage = ' '#assume its brand new??
    #         else:
    #             mileage = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold').text
            
    #         vin = vins[vincount]    
    #         row = [make, model, year, mileage, price, vin, carpage]

    #         w.writerow(row)
    #         vincount+=1
    #         # url = getNextPage(soup)
    #         # if url == None:
    #         #     break

#edmunds.com
def Scrape4(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    
    minyear = str(int(year) - 5)
    maxyear = str(int(year) + 5)
    
    url = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used&make='+make+'&model='+model+'&radius=50&year='+minyear+'-'+maxyear+''
    # search first 10 pages
    with open('cardata4.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url']
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

                row = [make, model, trim, year, mileage, price, vin, carpage]

                w.writerow(row)
            url = getNextPage4(soup)
            if url == None:
                break 

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

#edmunds.com
def getNextPage4(soup):
    # page = soup.find('div', class_='sds-pagination__controls')
    next = soup.find('a', class_="pagination-btn rounded d-flex align-items-center justify-content-center text-primary-darker mx-1_5")
    # if next == None: 
    #     next = soup.find('a', id="next_paginate")
    url = 'http://www.edmunds.com' + str(next.get('href'))
    if url == 'http://www.edmunds.comNone':
        print('no next page')
        return None
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
    minYear = (str(int(year)- 5))
    maxYear = (str(int(year)+ 5))

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'woodbridge-va-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear=' + minYear + '&endYear=' + maxYear + '&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'

    with open('carvins2.csv', 'w', encoding='utf8', newline='') as f:
        vins = []
        # for n in range(1):
        page = requests.get(url)
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
    

Scrape4('Jeep', 'Wrangler', '2007', '22043')
# ScrapeVin2('Toyota', 'Camry', '2014', '22043')