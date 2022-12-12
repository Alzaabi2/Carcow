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
import random


#This Version of Scrape will be used to scrape all models across the washington DC area


#Cars.com
def Scrape1(make):

    make = make.lower().replace(' ', '_')
    
    # url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=100&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    url = 'https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D='+make+'&models%5B%5D=&list_price_max=&page_size=100&maximum_distance=50&zip=20001'
    # vins = ScrapeVin(make)
    
    scrapedList = []
    
    # search first 10 pages
    with open('cardata.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        # page = requests.get(url)
        while url != None:
            rand = random.random()
            time.sleep(rand*10)
            print(url)
            # headers = {
            #     'Accept': 'aplication/json',
            #     'Authorization': 'Basic VTAwMDAwOTA5MTg6Q2FyY293MTIz',
            #     # Already added when you pass json= but not when you pass data=
            #     'Content-Type': 'application/json',
            # }
            
            # json_data = {
            #     'target': 'universal',
            #     'parse': False,
            #     'url': url,
            # }

            # page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data)
            
            # p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
            p = requests.get(url)
            soup = BeautifulSoup(p.content, 'html.parser')
            cars = soup.find_all('div', class_="vehicle-card")
        
            for c in cars:
                if not c.find('h2', class_="title"):
                    continue
                title = c.find('h2', class_="title").text
                title = title.split(' ', 3)
                year = title[0]
                make = title[1]
                model = title[2]
                trim = title[3]
                
                if not c.find('span', class_="primary-price"):
                    continue
                price = c.find('span', class_="primary-price").text
                
                if not c.find('a', class_="vehicle-card-link js-gallery-click-link"):
                    continue
                carpage = 'http://cars.com' + c.find('a', class_="vehicle-card-link js-gallery-click-link").get('href')

                if not c.find('div', class_="mileage"):
                    mileage = ' '#assume its brand new??
                else:
                    mileage = c.find('div', class_="mileage").text
                
                try:
                    currentCarPage = requests.get(carpage)
                except:
                    # print('carpage error')
                    continue
                
                currentCarSoup = BeautifulSoup(currentCarPage.content, 'html.parser')
                imgDiv = currentCarSoup.find('img', class_="swipe-main-image image-index-0")
                if imgDiv is not None:
                    img = imgDiv.get('src')
                else:
                    img = ''
                
                # dom = etree.HTML(str(currentCarSoup))
                # vinPath = dom.xpath('/html/body/section/div[5]/div[2]/section[1]/dl/dd')
                try:
                    vinPath = currentCarSoup.find('dl', class_='fancy-description-list')
                    vinPath2 = vinPath.find_all('dd')
                    # print(vinPath)
                    vin = []
                    for i in vinPath2:
                        vinMatch = re.search(r'[0-9A-Z]{17}', i.text)
                        if vinMatch != None:
                            vin.append(vinMatch.group())
                except:
                    # print('vin error')
                    continue
                
                #special case for teslas
                if make.lower() == 'tesla':
                    if model.lower().replace(' ', '') == 'model':
                        trimSplit = trim.split(' ', 1)
                        model = model + ' ' + trimSplit[0]
                        if len(trimSplit) > 1:
                            trim = trimSplit[1]
                        else:
                            trim = ''
                            
                #special case for land rover 
                if make.lower() == 'land':
                    make = 'Land Rover'
                    if model.lower().replace(' ', '') == 'rover' and 'range rover' in trim.lower():
                        trimSplit = trim.split(' ', 2)
                        model = 'Range Rover'
                        if len(trimSplit) > 2:
                            trim = trimSplit[2] 
                        else:
                            trim = ''
                    elif model.lower().replace(' ', '') == 'rover':
                        trimSplit = trim.split(' ', 1)
                        model = trimSplit[0]
                        if len(trimSplit) > 1:
                            trim = trimSplit[1] 
                        else:
                            trim = ''     
                                          
                # print(vin)
                # if len(vinPath) == 0:
                #     vin = ''
                #     print('Path: ' + vinPath)
                # else:
                #     vin = vinPath[0].text
                #     if vin
                # print(vin)
                if len(vin) == 0:
                    continue
                vin2 = vin[0]
                row = [make, model, trim, year, mileage, price, vin2, carpage, img]
                rowlist = {'Make': make, 'Model':model, 'Trim':trim, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin2, 'url':carpage, 'img':img}
                w.writerow(row)
                scrapedList.append(rowlist)
            url = getNextPage(soup)
            print(url)
            
    return scrapedList


#Autotrader.com
def Scrape2(make, model):

    zipcode = '20001'
    make = make.lower().replace(' ', '_')
    model = model.lower().replace(' ', '_')
    
    zipdata = json.loads(getZipData(zipcode))
    city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
    state = str(zipdata['results'][zipcode][0]['state_code'])

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/washington-dc-20001?requestId=USED&dma=&searchRadius=50&location=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    vins = ScrapeVin2(make, model)
    scrapedList = []
    with open('cardata2.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url', 'img']
        w.writerow(header)
        vincount = 0
        while url != None:
            print(url)
            page = requests.get(url, timeout=10000)
            soup = BeautifulSoup(page.content, 'html.parser') 
            cars = soup.find_all('div', class_="item-card row display-flex align-items-stretch")
            for c in cars:
                # print('-----')
                if c == None:
                    continue
                if c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled") == None:
                    continue
                title = c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled").text
                if "New" in title:
                    continue
                title = title.split(' ', 4)
                year = title[1]
                make = title[2]
                model = title[3]
                if len(title) < 5:
                    trim = ''
                else:
                    trim = title[4]
                
                if c.find('span', class_="first-price") == None:
                    continue
                price = c.find('span', class_="first-price").text
                carpage = 'https://www.autotrader.com' + c.find('a', rel="nofollow").get('href')
                currentCarPage = requests.get(carpage)
                currentCarSoup = BeautifulSoup(currentCarPage.content, 'html.parser')
                imgDiv = c.find('img', class_="carousel-image css-1tknha6-StyledImage e1nnhggb0")
                if imgDiv is not None:
                    img = imgDiv.get('src')
                else:
                    imgDiv = currentCarSoup.find('img', class_="img-responsive media-gallery-image")
                    if imgDiv is not None:
                        img = imgDiv.get('src')
                    else:
                        img = ''

                if c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter"):
                    mileageDivider = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter")
                    if not mileageDivider.find('span', class_='text-bold'):
                        mileage = ' '#assume its brand new??
                    else:
                        mileage = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold').text
                else:
                    mileage = ' '
                
                # if c.find('img', class_='image-vertically-aligned') is None:
                #     img = ''
                #     print('no pic')
                # else:
                #     img = c.find('img', class_='image-vertically-aligned').get('src')

                # print(img)
                vin = vins[vincount]    
                #special case for teslas
                if make.lower() == 'tesla':
                    if model.lower().replace(' ', '') == 'model':
                        trimSplit = trim.split(' ', 1)
                        model = model + ' ' + trimSplit[0]
                        if len(trimSplit) > 1:
                            trim = trimSplit[1]
                        else:
                            trim = ''
                #special case for land rover 
                if make.lower() == 'land':
                    print(make)
                    print(model)
                    print(trim)
                    make = 'Land Rover'
                    if model.lower().replace(' ', '') == 'rover' and 'range rover' in trim.lower():
                        trimSplit = trim.split(' ', 2)
                        model = 'Range Rover'
                        if len(trimSplit) > 2:
                            trim = trimSplit[2] 
                        else:
                            trim = ''
                    elif model.lower().replace(' ', '') == 'rover':
                        trimSplit = trim.split(' ', 1)
                        model = trimSplit[0]
                        if len(trimSplit) > 1:
                            trim = trimSplit[1] 
                        else:
                            trim = ''     
                                 
                row = [make, model, trim, year, mileage, price, vin, carpage, img]
                rowlist = {'Make': make, 'Model':model, 'Trim':trim, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage, 'img':img}
                w.writerow(row)
                scrapedList.append(rowlist)
                vincount+=1
            url = getNextPage2(soup)
    return scrapedList

# #Autotrader.com
# def Scrape2(make):

#     make = make.lower()
    
#     # zipdata = json.loads(getZipData(zipcode))
#     # city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
#     # state = str(zipdata['results'][zipcode][0]['state_code'])

#     url = 'https://www.autotrader.com/cars-for-sale/'+make+'/washington-dc-20001?dma=&searchRadius=50&location=&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
#     vins = ScrapeVin2(make)
#     scrapedList = []
#     # search first 10 pages
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
#     browser.get(url)
#     nextPage = True
#     while nextPage is not None:
#         with open('cardata2.csv', 'w', encoding='utf8', newline='') as f:
#             w = writer(f)
#             header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
#             w.writerow(header)
#             vincount = 0
#             # page = requests.get(url, timeout=10000)
            
#             # headers = {
#             #     'Accept': 'html',
#             #     'Authorization': 'Basic VTAwMDAwODk4NzQ6U2FpZjIwMDI=',
#             #     # Already added when you pass json= but not when you pass data=
#             #     # 'Content-Type': 'application/json',
#             # }

#             # json_data = {
#             #     'target': 'universal',
#             #     'parse': False,
#             #     'url': url,
#             # }

#             # page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data, timeout=10)
#             # p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
#             # print(url)
            
#             soup = BeautifulSoup(browser.page_source, 'html.parser')
            
#             cars = soup.find_all('div', class_="item-card-body margin-bottom-auto")
#             for c in cars:
#                 if c == None:
#                     continue
#                 if c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled") == None:
#                     continue
#                 title = c.find('h2', class_="text-bold text-size-400 text-size-sm-500 link-unstyled").text
#                 title = title.split(' ')
#                 year = title[1]
#                 make = title[2]
#                 model = title[3]
#                 if c.find('span', class_="first-price") == None:
#                     continue
#                 price = c.find('span', class_="first-price").text
#                 carpage = 'https://www.autotrader.com' + c.find('a', rel="nofollow").get('href')
#                 if c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter"):
#                     mileageDivider = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter")
#                     if not mileageDivider.find('span', class_='text-bold'):
#                         mileage = ' '#assume its brand new??
#                     else:
#                         mileage = c.find('div', class_="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter").find('span', class_='text-bold').text
#                 else:
#                     mileage = ' '
#                 vin = vins[vincount]    
#                 row = [make, model, year, mileage, price, vin, carpage]
#                 rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
#                 w.writerow(row)
#                 scrapedList.append(rowlist)
#                 vincount+=1
#             next_page_button = browser.find_element(By.XPATH, '//*[@id="ae_jim_pagination877"]/li[8]/a')
#             if next_page_button is not None:
#                 next_page_button.click()
#             else:
#                 nextPage = False
            
#     return scrapedList



#cargurus.com
def Scrape3(make):
    scrapedList = []
    # year = int(year)
    zipcode = '20001'
    makesRequest = requests.get('https://www.cargurus.com/Cars/api/1.0/carselector/listMakes.action')
    makesList = json.loads(makesRequest.content)['makes']
    makeIDs = {}
    for n in makesList:
        name = n['name'].lower()
        makeIDs[name] = n['id']
    
    makeID = makeIDs[make.lower()]
    
    # modelsRequest = requests.get('https://www.cargurus.com/Cars/api/1.0/carselector/listModels.action?searchType=USED&makeId='+makeID)
    # modelsList = json.loads(modelsRequest.content)['models']
    # modelIDs = {}
    # for n in modelsList:
    #     name = n['name'].lower()
    #     modelIDs[name] = n['id']
        
    # modelID = modelIDs[model.lower()]
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    url = 'https://www.cargurus.com/Cars/api/1.0/carselector/listingSearch.action?searchType=USED&entityId='+makeID+'&postalCode='+zipcode+'&distance=50'
    browser.get(url)
    # minYear = browser.find_element(By.CSS_SELECTOR, "[aria-label='Select Minimum Year']")
    # minYearInput = Select(minYear)
    # minYeartext = year - 5
    # minYeartext = str(minYeartext)
    # minYearInput.select_by_visible_text(minYeartext)
    
    # maxYear = browser.find_element(By.CSS_SELECTOR, "[aria-label='Select Maximum Year']")
    # maxYearInput = Select(maxYear)
    #make sure year is not over current year
    # maxYeartext = year + 5
    # date = datetime.date.today()
    # if maxYeartext > int(date.strftime("%Y")):
    #     maxYeartext = int(date.strftime("%Y")) + 1
    # maxYeartext = str(maxYeartext)
    # minYeartext = str(minYeartext)
    
    # time.sleep(2.5)#wait for year to update
    # try:
    #     maxYearInput.select_by_visible_text(maxYeartext)
    # except: 
    #     if maxYeartext == '2023':
    #         maxYeartext = '2022'
    #     maxYearInput.select_by_visible_text(maxYeartext)
    # minYearInput.select_by_visible_text(minYeartext)
    # time.sleep(2.5)
    # p = requests.get('https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity=m32&distance=50&zip=10002&sourceContext=carSelectorAPI', timeout=5000)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # print(soup.encode("utf-8"))
    numCars = soup.find('span', class_='eegHEr').find_all('strong')[1].text
    print(numCars)
    numPages = round(int(numCars.replace(',',''))/15)
    print(numCars + ' - ' + str(numPages))
    # numPages = 6
    with open('cardata3.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url', 'img']
        w.writerow(header)
        
        for i in range(numPages):
            # soup = BeautifulSoup(browser.page_source, 'html.parser')
            # headers = {
            #     'Accept': 'html',
            #     'Authorization': 'Basic VTAwMDAwODk4NzQ6U2FpZjIwMDI=',
            #     # Already added when you pass json= but not when you pass data=
            #     # 'Content-Type': 'application/json',
            # }

            # json_data = {
            #     'target': 'universal',
            #     'parse': False,
            #     'url': url,
            # }

            # page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data)
            # p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
            # p = requests.get(url)
            try:
                browser.get(url)
            except: 
                break
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
                    if c == None:
                        continue
                    if c.find('p', class_='JKzfU4 umcYBP') == None:
                        continue
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
                    carpage = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity='+makeID+'&distance=50&zip='+zipcode+'&sourceContext=carSelectorAPI' + carpagepart
                    priceText = c.find('span', class_='JzvPHo')
                    if priceText is not None:
                        price = priceText.text.split(' ', 1)
                        price = price[0]
                    else:
                        price = ''
                    
                    if c.find('img', class_='C6f2e2 bmTmAy') is None:
                        img = ''
                    else:
                        img = c.find('img', class_='C6f2e2 bmTmAy').get('src')
                        if '.svg' in img:
                            img = ''
                    #special case for teslas
                    if make.lower() == 'tesla':
                        if model.lower().replace(' ', '') == 'model':
                            trimSplit = trim.split(' ', 1)
                            model = model + ' ' + trimSplit[0]
                            if len(trimSplit) > 1:
                                trim = trimSplit[1]
                            else:
                                trim = ''
                    #special case for land rover 
                    if make.lower() == 'land':
                        print(make)
                        print(model)
                        print(trim)
                        make = 'Land Rover'
                        if model.lower().replace(' ', '') == 'rover' and 'range rover' in trim.lower():
                            trimSplit = trim.split(' ', 2)
                            model = 'Range Rover'
                            if len(trimSplit) > 2:
                                trim = trimSplit[2] 
                            else:
                                trim = ''
                        elif model.lower().replace(' ', '') == 'rover':
                            trimSplit = trim.split(' ', 1)
                            model = trimSplit[0]
                            if len(trimSplit) > 1:
                                trim = trimSplit[1] 
                            else:
                                trim = ''     
                    
                    row = [make, model, trim, year, mileage, price, vin, carpage, img]
                    rowlist = {'Make': make, 'Model':model, 'Trim':trim, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage, 'img':img}
                    w.writerow(row)
                    scrapedList.append(rowlist)
                    print(rowlist)
                print('scraped:' + str(len(scrapedList)))
                # next page
            else:
                break
            url = 'https://www.cargurus.com/Cars/api/1.0/carselector/listingSearch.action?searchType=USED&entityId='+makeID+'&postalCode='+zipcode+'&distance=50&sourceContext=carSelectorAPI#resultsPage=' + str(i+2)
            print(url)
            time.sleep(5)            
            
    return scrapedList


#edmunds.com
def Scrape4(make, model):
    scrapedList = []

    make = make.lower().replace(' ', '-')
    model = model.lower().replace(' ', '-')
    if make == 'tesla':
        model = model.replace('_', '-')
    elif make == 'land':
        make = make.replace('_', '-').replace
        model = model.replace('_', '-')
    
    url = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used&make='+make+'&model='+model+'&radius=50&deliverytype=local'
    # search first 10 pages
    with open('cardata4.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        # header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url', 'img']
        w.writerow(header)
        vincount = 0
        i = 1
        while url != None:
            print(url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

            page = requests.get(url, headers=headers)
            # soup = BeautifulSoup(page.content, 'html.parser')
            # headers = {
            #     'Accept': 'html',
            #     'Authorization': 'Basic VTAwMDAwODk4NzQ6U2FpZjIwMDI=',
            #     # Already added when you pass json= but not when you pass data=
            #     # 'Content-Type': 'application/json',
            # }

            # json_data = {
            #     'target': 'universal',
            #     'parse': False,
            #     'url': url,
            # }

            # page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data)
            # p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
            soup = BeautifulSoup(page.content, 'html.parser')
            
            cars = soup.find_all('div', class_="d-flex flex-column usurp-inventory-card w-100 srp-expanded")
            if len(cars) < 2:
                break
            i += 1
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
                img_cont = c.find('figure', class_='usurp-inventory-card-photo-image pos-r m-0')
                if img_cont == None:
                    continue
                img = img_cont.find('img')
                if img == None:
                    continue
                img_link = img.get('src')
                
                if c.find('div', class_='font-weight-normal size-14 text-gray-dark') == None:
                    trim = ''
                else:
                    trim = c.find('div', class_='font-weight-normal size-14 text-gray-dark').text
                
                mileage = c.find('span', class_='').text
                title = title.split(' ')
                year = title[0]
                make = title[1]
                model = title[2]
                if make.lower() == 'tesla' and len(title) >= 4:
                    model = model + ' ' + title[3]
                if make.lower() == 'land' and len(title) >= 4:
                    make = 'Land Rover'
                    model = title[3]
                    if model.lower() == 'range':
                        model = 'Range Rover'
                        
                link = c.find('a', class_='usurp-inventory-card-vdp-link').get('href')
                carpage = 'https://www.edmunds.com'+link
                parseLink = link.split('/')
                vin = parseLink[5]

                row = [make, model, trim, year, mileage, price, vin, carpage, img_link]
                # row = [make, model, year, mileage, price, vin, carpage, img]
                rowlist = {'Make': make, 'Model':model, 'Trim':trim, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage, 'img':img_link}
                w.writerow(row)
                scrapedList.append(rowlist)
                modelurl = model.replace(' ', '-')
                makeurl = make.replace(' ', '-')
                
            url = 'https://www.edmunds.com/inventory/srp.html?inventorytype=used&make='+makeurl+'&model='+modelurl+'&radius=50&pagenumber='+str(i)+'&deliverytype=local'
    # print('Scrape4 returning '+str(len(scrapedList))+' cars')
    return scrapedList

#carsdirect.com
# def Scrape5():
#     scrapedList = []
#     # make = make.lower()
#     # model = model.lower()
    
#     # minyear = str(int(year) - 5)
#     # maxyear = str(int(year) + 5)
    
#     # url = 'https://www.carsdirect.com/used_cars/listings/' + make + '/' + model + '?zipcode=' + zipcode + '&dealerId=&distance=&yearFrom=' + minyear + '&yearTo=' + maxyear + '&priceFrom=&priceTo=&qString=' + make + '%603%6020%600%600%60false%7C' + model + '%604%60380%600%600%60false%7C&keywords=&makeName=' + make + '&modelName=' + model + '&sortColumn=&sortDirection=&searchGroupId=&lnk='
#     url = 'https://www.carsdirect.com/used_cars/listings?zipcode=20001&distance=50&qString=&keywords=&pageNum=1&sortColumn=Default&sortDirection=ASC&makeName='
#     with open('cardata5.csv', 'w', encoding='utf8', newline='') as f:
#         w = writer(f)
#         # header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url']
#         header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
#         w.writerow(header)
#         vincount = 0
#         while url != None:
#             print(url)
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

#             page = requests.get(url, headers=headers)
#             soup = BeautifulSoup(page.content, 'html.parser')
#             # headers = {
#             #     'Accept': 'html',
#             #     'Authorization': 'Basic VTAwMDAwODk4NzQ6U2FpZjIwMDI=',
#             #     # Already added when you pass json= but not when you pass data=
#             #     # 'Content-Type': 'application/json',
#             #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
#             #     "Upgrade-Insecure-Requests": "1",
#             #     "DNT": "1",
#             #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             #     "Accept-Language": "en-US,en;q=0.5",
#             #     "Accept-Encoding": "gzip, deflate"
#             # }

#             # json_data = {
#             #     'target': 'universal',
#             #     'parse': False,
#             #     'url': url,
#             # }

#             # page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data)
#             # p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
#             # soup = BeautifulSoup(p, 'html.parser')
            
#             cars = soup.find_all('div', class_="list-row")
#             for c in cars:
#                 title = c.find('span', class_='listing-header').text
#                 title = title.split(' ')
#                 year = title[0]
#                 make = title[1]
#                 model = title[2]
#                 if c.find('a', class_='detail-price').find('span') is None:
#                     continue
#                 price = c.find('a', class_='detail-price').find('span').text
#                 if c.find('div', class_="mileage").find('span') is None:
#                     continue
#                 mileage = c.find('div', class_="mileage").find('span').text
#                 if c.find('span', class_='trimspan') is None:
#                     continue
#                 trim = c.find('span', class_='trimspan').text
#                 if c.find('span', class_='WrapperButtonSave') is None:
#                     continue
#                 vin = c.find('span', class_='WrapperButtonSave').get('vin')
#                 if c.find('meta') is None:
#                     continue
#                 carpage = c.find('meta').get('content')
#                 url = 'https://www.carsdirect.com' + carpage
                
#                 # row = [make, model, trim, year, mileage, price, vin, url]
#                 row = [make, model, year, mileage, price, vin, carpage]
#                 rowlist = {'Make': make, 'Model':model, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage}
#                 print(row)
#                 w.writerow(row)
#                 scrapedList.append(rowlist)
#             url = getNextPage5(soup)
#             if url == None:
#                 break 
#     return scrapedList

#carsdirect.com
def Scrape5(make, model):
    scrapedList = []
    make = make.lower().replace(' ', '-')
    model = model.lower().replace(' ', '-')
    if make == 'tesla':
        model = model.replace('_', '-')
    elif make == 'land':
        make = make.replace('_', '-').replace
        model = model.replace('_', '-')
    
    url = 'https://www.carsdirect.com/used_cars/listings/' + make + '/' + model + '?zipcode=' + '20001' + '&dealerId=&distance=50&yearFrom=&yearTo=&priceFrom=&priceTo=&qString=' + make + '%603%6020%600%600%60false%7C' + model + '%604%60380%600%600%60false%7C&keywords=&makeName=' + make + '&modelName=' + model + '&sortColumn=&sortDirection=&searchGroupId=&lnk='
    # search first 3 pages
    with open('cardata5.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Trim', 'Year', 'Mileage', 'Price', 'VIN', 'url', 'img']
        # header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
        w.writerow(header)
        vincount = 0
        while url != None:
            print(url)
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
                if make.lower() == 'tesla' and len(title) >= 4:
                    model = model + ' ' + title[3]
                if make.lower() == 'land' and len(title) >= 4:
                    make = 'Land Rover'
                    model = title[3]
                    if model.lower() == 'range':
                        model = 'Range Rover'
                
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
                if c.find('a', class_='list-img') is None:
                    img = ''
                else:
                    img = c.find('a', class_='list-img').find('span').find('img').get('src')
                
                if c.find('span', class_='trimspan') is None:
                    trim = ''
                else:
                    trim = c.find('span', class_='trimspan').text
                
                
                carpage = c.find('meta').get('content')
                carpage = 'https://www.carsdirect.com' + carpage
                
                # row = [make, model, trim, year, mileage, price, vin, url]
                row = [make, model,trim, year, mileage, price, vin, carpage, img]
                rowlist = {'Make': make, 'Model':model, 'Trim':trim, 'Year':year, 'Mileage':mileage, 'Price':price, 'VIN':vin, 'url':carpage, 'img':img}
                w.writerow(row)
                scrapedList.append(rowlist)
            url = getNextPage5(soup)
            if url == None:
                break 
    return scrapedList


#cars.com       
def getNextPage(soup):
    if soup is None:
        return None
    page = soup.find('div', class_='sds-pagination__controls')
    if page is None:
        return None
    next = page.find('button', id="next_paginate")
    if next == None: 
        next = page.find('a', id="next_paginate")
    url = 'http://cars.com' + str(next.get('href'))
    if url == 'http://cars.comNone':
        # print('no next page')
        return None
    return url

#autotrader.com       
def getNextPage2(soup):
    if soup is None:
        return None
    page = soup.find('div', class_='sds-pagination__controls')
    if page is None:
        return None
    next = page.find('button', id="next_paginate")
    if next == None: 
        next = page.find('a', id="next_paginate")
    url = 'http://autotrader.com' + str(next.get('href'))
    if url == 'http://autotrader.comNone':
        # print('no next page')
        return None
    
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
def ScrapeVin(make):
    make = make.lower()
    # url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=100&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    url = 'https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D='+make+'&models%5B%5D=&list_price_max=&page_size=100&maximum_distance=50&zip=20001'
    
    with open('carvins.csv', 'w', encoding='utf8', newline='') as f:
        vins = []
        while url is not None:
            headers = {
                'Accept': 'html',
                'Authorization': 'Basic VTAwMDAwODk4NzQ6U2FpZjIwMDI=',
                # Already added when you pass json= but not when you pass data=
                # 'Content-Type': 'application/json',
            }

            json_data = {
                'target': 'universal',
                'parse': False,
                'url': url,
            }

            page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data)
            p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
            soup = BeautifulSoup(p, 'html.parser')
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
            print(url)
                
    return vins



#autotrader.com
def ScrapeVin2(make,model):
    make = make.lower()
    model = model.lower()
    zipcode = '20001'

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/washington-dc-20001?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
    with open('carvins2.csv', 'w', encoding='utf8', newline='') as f:
        vins = []
        while url != None:
            page = requests.get(url, timeout=10000)
            soup = BeautifulSoup(page.content, 'html.parser') 
            searchContent = soup.find_all('script')
            for n in searchContent:
                if 'vehicleIdentificationNumber' in n.text:
                    j = json.loads(n.text)
                    vins.append(j['vehicleIdentificationNumber'])
                    f.write(j['vehicleIdentificationNumber'])
                    f.write('\n')
            url = getNextPage2(soup)
    return vins


# #autotrader.com
# def ScrapeVin2(make):
    

#     url = 'https://www.autotrader.com/cars-for-sale/'+make+'/washington-dc-20001?dma=&searchRadius=50&location=&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=100'
#     with open('carvins2.csv', 'w', encoding='utf8', newline='') as f:
#         vins = []
#         # for n in range(1):
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
#         browser.get(url)
#         print(browser.page_source)
#         nextPage = True
#         while nextPage is True:
#             # page = requests.get(url, timeout=10000)
#             soup = BeautifulSoup(browser.page_source, 'html.parser') 
#             # headers = {
#             #     'Accept': 'html',
#             #     'Authorization': 'Basic VTAwMDAwODk4NzQ6U2FpZjIwMDI=',
#             #     # Already added when you pass json= but not when you pass data=
#             #     # 'Content-Type': 'application/json',
#             # }

#             # json_data = {
#             #     'target': 'universal',
#             #     'parse': False,
#             #     'url': url,
#             # }

#             # page = requests.post('https://scrape.smartproxy.com/v1/tasks', headers=headers, json=json_data, timeout=10)
#             # p = str(page.content).replace('\\n', '').replace('\\', '').replace("b'", '').replace('{"results":[{"content":"', '')
#             # soup = BeautifulSoup(p, 'html.parser')
            
#             searchContent = soup.find_all('script')
#             for n in searchContent:
#                 if 'vehicleIdentificationNumber' in n.text:
#                     j = json.loads(n.text)
#                     vins.append(j['vehicleIdentificationNumber'])
#                     f.write(j['vehicleIdentificationNumber'])
#                     f.write('\n')
                    
#             next_page_button = browser.find_element(By.XPATH, '//*[@id="ae_jim_pagination877"]/li[8]/a')
#             if next_page_button is not None:
#                 next_page_button.click()
#                 print(nextPage)
#             else:
#                 nextPage = False
#     return vins

        
# def ScrapeToList(make, model, year, zipcode):
#     make = make.lower()
#     model = model.lower()
#     url = 'https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D=' + make + '&models%5B%5D=' + make + '-' + model +'&list_price_max=&maximum_distance=20&zip=' + zipcode
#     url2 = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=20&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
#     page = requests.get(url2)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     cars = soup.find_all('div', class_="vehicle-card")
#     ret_list = []
#     for c in cars:
#         title = c.find('h2', class_="title").text
#         title = title.split(' ', 2)
#         year = title[0]
#         make = title[1]
#         model = title[2]
#         price = c.find('span', class_="primary-price").text
#         mileage = c.find('div', class_="mileage").text
#         row = [make, model, year, mileage, price]
#         ret_list.append(row)
#     return ret_list


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

def ScrapeAlpha(make, model, year, zipcode):
    try:
        l1 = Scrape1(make, model, year, zipcode) 
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

#removes duplicate data
def cleanData(list):
    print(list)
    print('results list')
    res_list = []
    for i in range(len(list)):
        if list[i] not in list[i + 1:]:
            res_list.append(list[i])
            
    return res_list      
    
    
l = Scrape5('land rover', 'range rover')
print(l)
print(str(len(l)))


# Scrape1('land_rover')
# ScrapeAlpha('Jeep', 'Wrangler', '2014', '10003')