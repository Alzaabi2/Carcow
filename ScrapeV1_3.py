import string
from bs4 import BeautifulSoup
import requests
from csv import writer
import json

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
        for n in range(10):
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
            url = getNextPage(soup)
            if url == None:
                break

#Autotrader.com
def Scrape2(make, model, year, zipcode):

    make = make.lower()
    model = model.lower()
    
    zipdata = json.loads(getZipData(zipcode))
    city =str(zipdata['results'][zipcode][0]['city']).replace(' ', '')
    state = str(zipdata['results'][zipcode][0]['state_code'])

    url = 'https://www.autotrader.com/cars-for-sale/all-cars/'+make+'/'+model+'/'+city+'-'+state+'-'+zipcode+'?requestId=2152820002&dma=&searchRadius=50&location=&marketExtension=include&startYear='+year+'&endYear='+year+'&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100'

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
    

Scrape2('Jeep', 'Wrangler', '2020', '22043')
# ScrapeVin2('Toyota', 'Camry', '2014', '22043')




