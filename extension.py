from bs4 import BeautifulSoup
import requests

#returns car data for car viewed in the browser
def singleCarData(url):
    #get page html
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #find title text from class
    title = soup.find('h1', class_='listing-title').text #always use _class in BS
    print(title)
    title = title.split(' ', 3)
    #find make
    make = title[1]
    print (make)
    #find model
    model = title[2]
    print (model)
    #find year
    year = title[0]
    print(year)
    #find trim(optional)
    trim = title[3]
    print(trim)

    entry = "Make: " + make + " --- Model: " + model + " ---Trim: " + trim + " --- Year: " + year
    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    carEntry = {}
    carEntry[make + " Entry"] = entry
    print (carEntry)
    return carEntry

singleCarData('https://www.cars.com/vehicledetail/0f0931d4-0926-4ab5-9464-bb38a6b5cbdc/')