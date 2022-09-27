import rateV1
from bs4 import BeautifulSoup
import requests
from csv import writer

#This version of Scrape works on cars.com, it takes car specifications and outputs a csv file
# with the first 20 car search results. Each car will be described by Make,Model,Year,Mileage,Price.
# The scraping api used is BeautifulSoup

#working
def Scrape(make, model, year, zipcode):
    make = make.lower()
    model = model.lower()
    url = 'https://www.cars.com/shopping/results/?stock_type=used&makes%5B%5D=' + make + '&models%5B%5D=' + make + '-' + model +'&list_price_max=&maximum_distance=20&zip=' + zipcode
    url2 = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=' + make + '&maximum_distance=20&models[]=' + make + '-' + model +'&page=1&page_size=100&stock_type=used&zip=' + zipcode
    page = requests.get(url2)
    soup = BeautifulSoup(page.content, 'html.parser')
    cars = soup.find_all('div', class_="vehicle-card")
    # print(page.content)
    with open('cardata.csv', 'w', encoding='utf8', newline='') as f:
        w = writer(f)
        header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'Trim', 'Suggested Price', 'Deal score']
        w.writerow(header)
        for c in cars:
            title = c.find('h2', class_="title").text
            # print(title)
            title = title.split(' ', 3)
            year = title[0]
            make = title[1]
            model = title[2]
            trim = title[3]
            price = c.find('span', class_="primary-price").text
            mileage = c.find('div', class_="mileage").text
            a = mileage.split(' ', 1) # takes out 'mi' from the end of mileage
            m = a[0]
            suggested = rateV1.dollarValue(make, model, year, m, zipcode)
            suggested = suggested.replace(',', '')
            price = price.replace(',', '')
            suggested = suggested.replace('$', '')
            price = price.replace('$', '')
            ratio = int(suggested)/int(price) #metric for rating deal
            row = [make, model, year, mileage, price, trim, suggested, ratio]
            w.writerow(row)
        
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
#         suggested = rateV1.dollarValue(make, model, year, mileage, zipcode)
#         row = [make, model, year, mileage, price, suggested]
#         ret_list.append(row)
#     return ret_list

Scrape('Audi', 'A7', '2014', '22043')