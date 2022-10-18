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
    #find make
   
    #find model

    #find year

    #find trim(optional)

    #Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car

SingleCarData('https://www.cars.com/vehicledetail/0f0931d4-0926-4ab5-9464-bb38a6b5cbdc/')