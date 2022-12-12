from rateV1 import *
from bs4 import BeautifulSoup
import requests
import datetime

def getMSRP(make, model, trim, year):
    model = model.split(' ', 1)
    if trim == '' and len(model)>1:
        trim = model[1]
    trim = trim.lower().replace(' ', '')
    model = model[0]
    url = 'https://www.cars.com/research/'+make.lower()+'-'+model.lower()+'-'+year
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    if not soup.find('ul', class_='trim-compare-list'):
        return 0
    
    trimList = soup.find('ul', class_='trim-compare-list').findAll('li')
    for t in trimList:
        if not t.find('a'): continue
        page_trim =  t.find('a').text.lower().replace(' ', '')
        if page_trim == trim:
            price = t.find('p').text
            price = int(price.replace('$', '').replace(',', '').replace(' ', ''))
            return price
    
    #get first price if trim not found
    for t in trimList:
        if t.find('p') is not None:
            if '$' in t.find('p').text:
                price = t.find('p').text
                price = int(price.replace('$', '').replace(',', '').replace(' ', ''))
                return price
    

def finalValue(Make, Model, Trim, Year, noOwners, mileage, collisions):
    initVal = getMSRP(Make, Model, Trim, Year)
    if initVal is None:
        return 0
    date = datetime.date.today()
    age = int(date.strftime("%Y")) - int(year)
    
    localAge = age
    mileage = str(mileage)
    localMileage = int(mileage.replace(',', '').replace(' ', '').replace('mi', '').replace('les', '').replace('.', ''))
        
    localCollisions = collisions
    localInitVal = initVal
    
    lossMiles = calcDepreciation(initVal, 1000, localMileage, 150000, 0.2)
    lossCollisions = calcDepreciation(localInitVal, 1, localCollisions, 5, 2)
    lossOwners = 0
    if noOwners > 2:
        lossOwners = initVal * 0.25
    if age > 10:
        localAge = 10
    ageInMonths = localAge * 12
    lossAge = initVal * (ageInMonths * 0.005)
    
    adjustedValue = initVal - lossAge - lossCollisions - lossMiles - lossOwners
    if noOwners == 1:
        adjustedValue *= 1.1
    return adjustedValue

def calcDepreciation(value, step, causeValue, causeLimit, percentage):
    tempValue = value
    tempCauseValue = causeValue
    if causeValue == 0:
        return 0
    if causeValue > causeLimit:
        tempCauseValue == causeLimit
    i = 0
    while i<tempCauseValue:
        tempValue *= (1 - percentage/100)
        i+=step
        
    return value - tempValue
    

#Dodge Challenger Coupe R/T V8 2019 32,157 mi listed for $26,966
initVal = 34545
noOwners = 3
collisions = 0
year = 2019
age = 2022 - year
mileage = 32157

vin = '2C3CDZBT5KH524440'

# val = finalValue('Dodge', 'Challenger', 'R/T', '2021', noOwners, mileage, collisions)