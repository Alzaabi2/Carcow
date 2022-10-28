from bs4 import BeautifulSoup
import requests

#returns car data for car viewed in the browser
def singleCarData(url):
    print('got url')
    if(url == ''):
        print('no url')
        return
    #get page html
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #find title text from class
    title = soup.find('h1', class_='listing-title').text
    # .find('body', class_='loaded vsc-initialized ae-lang-en ae-device-desktop')
    # .find('main', class_='sds-page-container').find('div', class_='vdp-content-wrapper price-history-grid ').find('section', class_='listing-overview').find('header', class_='gallery-header').find('div', class_='title-section').find('h1', class_='listing-title') #always use _class in BS
    print("title:", title)
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
    carEntry[make + " Car Entry"] = entry
    print (carEntry)
    ret = '' + make + ' ' + model + ' ' + year
    return ret 

singleCarData('https://www.cars.com/vehicledetail/328daed2-aa5f-4882-bddc-d0bde3601e15')