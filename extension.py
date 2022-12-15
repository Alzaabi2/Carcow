from email import header
from time import sleep, time
from urllib import request
from bs4 import BeautifulSoup
import requests
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
import time
import http.client


#cars.com
#returns car data for car viewed in the browser
def singleCarData1(url):
    if(url == ''):
        return
    #get page html
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open('current.html', 'w', encoding='utf8', newline='') as f:
        f.write(str(soup))

    #find title text from class
    titleObj = soup.find('h1', class_='listing-title')
    if titleObj == None:
        titleObj = soup.find('h1', class_='sticky-header-listing-title')
    title = titleObj.text

    
    title = title.split(' ', 3)
    #find make
    make = title[1]

    #find model
    model = title[2]

    #find year
    year = title[0]

    #find trim(optional)
    trim = title[3]


    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    carEntry = {}
    carEntry['make'] = make
    carEntry['model'] = model
    carEntry['trim'] = trim
    carEntry['year'] = year
    ret = '' + make + ' ' + model + ' ' + year
    return carEntry

#autotrader.com
#returns car data for car viewed in the browser
def singleCarData2(url):
    if(url == ''):
        return
    url = url.replace('alllistingtype', 'allListingType').replace('listingid', 'listingId').replace('makecodelist', 'makeCodeList').replace('modelcodelist', 'modelCodeList').replace('requestid', 'requestId').replace('searchradius', 'searchRadius').replace('marketextension', 'marketExtension').replace('isnewsearch', 'isNewSearch').replace('showac', 'showAc').replace('used', 'USED')
    urlArr = url.split('makeCodeList=')
    temp = urlArr[1]
    urlArr = temp.split('modelCodeList=')
    makeCodeList = urlArr[0]
    url = url.replace(makeCodeList, makeCodeList.upper())


    temp = urlArr[1]
    urlArr = temp.split('city=')
    modelCodeList = urlArr[0]
    url = url.replace(modelCodeList, modelCodeList.upper())

    temp = urlArr[1]
    urlArr = temp.split('state=')
    city = urlArr[0]
    url = url.replace(city, city.capitalize())

    temp = urlArr[1]
    urlArr = temp.split('zip=')
    state = urlArr[0]
    url = url.replace(state, state.upper())

    #get page html
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    with open('currentPage.html', 'w', encoding='utf8', newline='') as f:
        f.write(str(soup))

    #find title text from class
    title = soup.find('h1', class_='text-bold text-size-400 text-size-sm-700 col-xs-12 col-sm-7 col-md-8').text
    
    title = title.split(' ', 4)
    #find make
    make = title[2]

    #find model
    model = title[3]

    #find year
    year = title[1]

    #find trim(optional)
    rawTrim = title[4]
    trim = rawTrim.split('w/')


    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    carEntry = {}
    carEntry['make'] = make
    carEntry['model'] = model
    carEntry['trim'] = trim[0]
    carEntry['year'] = year
    ret = '' + make + ' ' + model + ' ' + year + ' ' + trim[0]
    return carEntry

#cargurus.com
#returns car data for car viewed in the browser
def singleCarData3(url):
    if(url == ''):
        return

    #get page html
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    browser.get(url)
    
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    #find title text from class
    title = soup.find('h1', class_='IpF2YF').text

    # title = 'h h h h h h '
    title = title.split(' ',4)

    #find make
    make = title[1]
    if make.lower == 'tesla':
        model == 'Model' + title[3]
    else:
        #find model
        model = title[2]

    #find year
    year = title[0]

    #find trim(optional)
    rawTrim = title[3]
    trim = rawTrim.split('-')


    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    carEntry = {}
    carEntry['make'] = make
    carEntry['model'] = model
    carEntry['trim'] = trim[0]
    carEntry['year'] = year
    return carEntry

#edmunds.com
#returns car data for car viewed in the browser
def singleCarData4(url):
    if(url == ''):
        return
    #get page html
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    #find title text from class
    if soup.find('h1', class_='not-opaque text-black d-inline-block mb-0 size-24') is not None:
        title = soup.find('h1', class_='not-opaque text-black d-inline-block mb-0 size-24').text
    
    title = title.split(' ', 3)

    #find make
    make = title[1]
    if make.lower == 'tesla':
        model == 'Model' + title[3]
    else:
        #find model
        model = title[2]

    #find year
    year = title[0]

    #find trim(optional)
    trim = soup.find('span', class_='not-opaque text-black').text


    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    carEntry = {}
    carEntry['make'] = make
    carEntry['model'] = model
    carEntry['trim'] = trim[0]
    carEntry['year'] = year
    ret = '' + make + ' ' + model + ' ' + year + ' ' + trim
    return carEntry

#carsdirect.com
#returns car data for car viewed in the browser
def singleCarData5(url):
    if(url == ''):
        return

    #get page html
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    #find title text from class
    title = soup.find('div', class_='top-bar-title-set').find('h1').text
    
    title = title.split(' ', 3)

    #find make
    make = title[1]

    #find model
    model = title[2]

    #find year
    year = title[0]

    #find trim(optional)
    t = '?'
    tag_list = soup.find_all('dd')
    for t in tag_list:
        if t.get('itemprop') == 'vehicleConfiguration':
            trim = t.text

    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    carEntry = {}
    carEntry['make'] = make
    carEntry['model'] = model
    # carEntry['trim'] = trim[0]
    carEntry['year'] = year
    ret = '' + make + ' ' + model + ' ' + year + ' ' + trim
    return carEntry

# singleCarData1('https://www.cars.com/vehicledetail/328daed2-aa5f-4882-bddc-d0bde3601e15')
# singleCarData2('https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=659992633&allListingType=all-cars&startYear=2014&endYear=2014&year=&makeCodeList=NISSAN&modelCodeList=ALTIMA&city=New%20York&state=NY&zip=10003&location=&requestId=2281868035&searchRadius=100&marketExtension=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&dma=&referrer=%2Fcars-for-sale%2Fall-cars%2F2014%2Fnissan%2Faltima%2Fnew-york-ny-10003%3FrequestId%3D2281868035%26dma%3D%26searchRadius%3D100%26location%3D%26marketExtension%3Dinclude%26isNewSearch%3Dfalse%26showAccelerateBanner%3Dfalse%26sortBy%3Drelevance%26numRecords%3D100&clickType=spotlight')
# singleCarData3('https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?shopperListingsSearch=96715429#listing=340896159/PRIORITY')
# singleCarData4('https://www.edmunds.com/jeep/wrangler/2004/vin/1J4FA49S94P761541/')
# singleCarData5('https://www.carsdirect.com/used_cars/vehicle-detail/ul2154804725/ford/f-150?source=UsedCarListings&savedVehicleId=&recentSearchId=13132844')