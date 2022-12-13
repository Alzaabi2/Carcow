from ast import Continue
import csv
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import concurrent.futures
import itertools 
import json
from CarDepreciationValue import *

carlist = []


def main():

    # runs in 5 seconds per car:
    # print("threading")
    # list = createList()
    # with concurrent.futures.ThreadPoolExecutor() as executer:
    #     executer.map(dollarValueVin2, list)  

    demoDict = [{'Make': 'BMW', 'Model': '228i xDrive', 'Year': '2016', 'Mileage': '65,956', 'Price': '$24,950', 'VIN': 'WBA1G9C51GV599609', 'url': '1'},
                {'Make': 'BMW', 'Model': '228 Gran Coupe i xDrive', 'Year': '2021', 'Mileage': '24,681', 'Price': '$36,450', 'VIN': 'WBA73AK03M7H21242', 'url': '2'},
                {'Make': 'BMW', 'Model': '228 i', 'Year': '2014', 'Mileage': '56,547', 'Price': '$22,590', 'VIN': 'WBA1F5C50EV255231', 'url': '3'},
                {'Make': 'BMW', 'Model': '228i xDrive', 'Year': '2016', 'Mileage': '5,956', 'Price': '$2,950', 'VIN': 'WBA1G9C51GV599609', 'url': '4'},
                {'Make': 'BMW', 'Model': '228 Gran Coupe i xDrive', 'Year': '2021', 'Mileage': '124,681', 'Price': '$80,450', 'VIN': 'WBA73AK03M7H21242', 'url': '5'},
                {'Make': 'BMW', 'Model': '228 i', 'Year': '2014', 'Mileage': '756,547', 'Price': '$52,590', 'VIN': 'WBA1F5C50EV255231', 'url': '6'}]

    # print(demoDict)
    # dollarValue('Audi', 'A7', '2016', 130065, 22701) # Need to know which car from chrome extension
    # dollarValueVin('WAUP2AF20KN116129')
    

    #runs in 5 seconds per car:
    # print("threading")
    # list = createList()
    # with concurrent.futures.ThreadPoolExecutor() as executer:
    #     executer.map(dollarValueVin2, list)  
 
 
    # getTopCars test
    # deals = [('WBA1G9C51GV599609', 7.357627118644068), ('WBA73AK03M7H21242', 0.9995336076817558), ('WBA1G9C51GV599609', 0.869939879759519), ('WBA1F5C50EV255231', 0.700531208499336), ('WBA73AK03M7H21242', 0.45286513362336855), ('WBA1F5C50EV255231', 0.3009127210496292)]
    # deals = rate(createList())
    # list = createList()
    # deals = [('ZHWUC1ZD4ELA02158', 1.1615157732751988), ('ZHWUC1ZD0ELA02996', 1.0945740025740025), ('ZHWUC1ZD6ELA02419', 1.0391110222217417), ('ZHWUC1ZD0CLA00114', 0.9697389581524244), ('ZHWUG4ZD2HLA06039', 0.9664653979314289), ('ZHWUF3ZD8GLA04324', 0.5678466881216022), ('ZHWUR1ZD5ELA02331', 0.48796481503795636), ('ZHWUC1ZD0FLA03633', 0.48796481503795636), ('ZHWUR1ZD9FLA03502', 0.21584448056007)]
    # print(getTopCars(list, rate(list)))
 
    # listOfCars = createList()
    # print(listOfCars)
    # dollarValueVin('ZHWUC1ZD4ELA02158')

    # print(rate(createList()))
    # dollarValueVin3('ZHWUC1ZD4ELA02158')

    
    # list = createList()
    # count = 0
    # for i in range(len(list)):
    #     vin   = list[i]['VIN']
    #     print("No. ", count)
    #     suggested = dollarValueVin3(vin)
    #     time.sleep(1)
    #     count += 1


    # vinOnly = dollarValueVin3("1GYS4TKJ7FR633162")
    # print("VIN ONLY suggested price: ", vinOnly)

    # miles = 51000
    # vinAndMiles = dollarValueVin4("W1KUG6EB3LA528856", miles)
    # print("VIN AND MILEAGE suggested price: ", vinAndMiles)

    # print("From finalValue:")
    # rating1 = rate(createList())
    # print("Deals from using FinalValue function:", rating1)

    # print("\nFrom carUtils:")
    # rating2 = rate2(createList())
    # print("Deals from using Car Utils API:", rating2)

    # print("\nFrom new function:")
    # rating2 = rate3(createList())



    # dollarValueVin3("WAUYGAFC2DN090294")




def createList():
    csv_filename = 'cardata.csv'
    carlist =[]
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            carlist.append(row)
    
    return carlist


#incomplete
def rate(list):
    # carlist = createList()
    # print(list)
    deals = []
    if list is None:
        return []
    count = 1

    for i in range(len(list)):
    # for i in range(20):
        priceListed = list[i]['Price']
        vin   = list[i]['VIN']
        
        modelAndTrim = list[i]['Model']
        allWords = modelAndTrim.split(' ',1)
        model = allWords[0]
        trim = allWords[1]

        mileage = list[i]['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)


        # print("Price: ", priceListed, "Vin: ", vin)
        # suggested = dollarValueVin3(vin)
        suggested = finalValue(list[i]['Make'], model, trim, list[i]['Year'], 0, miles[0], 0)
        # suggested = suggested.replace(',', '')
        price = priceListed.replace(',', '')
        # suggested = suggested.replace('$', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')
        # print('no', i, 'p: ',price)
        
        try:
            ratio = float(suggested)/float(price) #metric for rating deal
        except: 
            ratio == 'No Ratio'

        row = (str(count), vin,ratio,priceListed)
        count += 1
        deals.append(row)
        # print("Ratio for vin ", vin, ": ", ratio)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: -y[2])
    print("\ndeals: ", deals)
    topDeals = [deals[0], deals[1], deals[2], deals[3], deals[4]]
    return topDeals

def rate2(list):
    # carlist = createList()
    # print(list)
    deals = []
    if list is None:
        return []
    count = 1

    for i in range(len(list)):
    # for i in range(20):
        priceListed = list[i]['price']
        vin   = list[i]['VIN']
        # print("Price: ", priceListed, "Vin: ", vin)

        mileage = list[i]['mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)

        suggested = dollarValueVin4(vin, miles[0])
        # suggested = suggested.replace(',', '')
        price = priceListed.replace(',', '')
        # suggested = suggested.replace('$', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')
        # print('no', i, 'p: ',price)
        
        try:
            ratio = float(suggested)/float(price) #metric for rating deal
        except: 
            ratio == 'No Ratio'
 
        row = (str(count), vin,ratio,priceListed)
        count += 1
        deals.append(row)
        # print("Ratio for vin ", vin, ": ", ratio)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: -y[2])
    print("\ndeals: ", deals)
    topDeals = [deals[0], deals[1], deals[2], deals[3], deals[4]]
    return topDeals

def rate3(list):
    # carlist = createList()
    # print(list)
    deals = []
    if list is None:
        return []
    count = 1

    for i in range(len(list)):
        price = list[i]['price']
        vin   = list[i]['VIN']
        # print("Price: ", priceListed, "Vin: ", vin)

        price = price.replace(',', '')
        # suggested = suggested.replace('$', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')

        ### Need to not include cars with suggested price of $0. Change here! ###
        suggested = list[i]['suggested']
        if suggested == '0':
            continue
        print("\nSuggested price is:\n", suggested, "and it's type is:", type(suggested))

        try:
            ratio = float(price)/float(suggested) #metric for rating deal
        except: 
            ratio == 'No Ratio'
 
        row = (str(count), vin,ratio,price)
        count += 1
        deals.append(row)
        # print("Ratio for vin ", vin, ": ", ratio)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: y[2])
    print("\ndeals: ", deals)
    topDeals = [deals[0], deals[1], deals[2], deals[3], deals[4]]
    return topDeals

# This is a temporary function for avoiding unavailable cars
def rate4(list):
    # carlist = createList()
    # print(list)
    deals = []
    if list is None:
        return []
    count = 1

    for i in range(len(list)):
        price = list[i]['price']
        vin   = list[i]['VIN']
        # print("Price: ", priceListed, "Vin: ", vin)

        price = price.replace(',', '')
        # suggested = suggested.replace('$', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')

        ### Need to not include cars with suggested price of $0. Change here! ###
        suggested = list[i]['suggested']
        if suggested == '0':
            continue
        # print("\nSuggested price is:\n", suggested, "and it's type is:", type(suggested))

        try:
            ratio = float(price)/float(suggested) #metric for rating deal
        except: 
            ratio == 'No Ratio'

        url = list[i]['url']
        
        row = (str(count), vin,ratio,price,url)
        count += 1
        deals.append(row)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: y[2])

    ret_list = []

    for car in range(len(deals)):
        if len(ret_list) >= 5:
            break
        url = deals[car][4]
        available = True
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        page = requests.get(url, headers=headers)
        # print("Got here!")
        soup = BeautifulSoup(page.content, 'html.parser')
        # print("Got here 1")
        if soup.find('p', class_='sds-notification__desc') is not None:
            available = False
            # print("Got here 2")
        elif soup.find('div', class_='text-bold text-size-600 text-size-sm-700 margin-vertical-7 margin-horizontal-7 text-center') is not None:
            # print("Got here 3")
            if soup.find('div', class_='text-bold text-size-600 text-size-sm-700 margin-vertical-7 margin-horizontal-7 text-center').text == 'This car is no longer available. One moment while we take you to the search results page.':
                available = False
                # print("Got here 4")
        elif soup.find('h2', class_='CVRsvD') is not None:
            available = False
            # print("Got here 5")
        elif soup.find('h2', class_='pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0') is not None:
            # print("Got here 6")
            if soup.find('h2', class_='pt-1 pt-md-3 px-1 px-md-3 pb-2 text-center display-1 m-0').text == 'Vehicle no longer available':
                available = False
                # print("Got here 7")
        elif soup.find('div', class_='CDCXWUsedCarBuyPathExpiredListingHeaderText widget') is not None:
            available = False
            # print("Got here 8")
        print("\navailable = ", available,)
        if available == True:
            # deals.remove(deals[car])
            ret_list.append(deals[car])
        else: 
            print('\nunavailable url: '+ url)

            
    # print("\ndeals: ", deals)
    # topDeals = [deals[0], deals[1], deals[2], deals[3], deals[4]]
    return ret_list

# #temp
# def rate(list):
#     # carlist = createList()

#     deals = []
#     for i in range(len(list)):
#         price = list[i]['Price']
#         vin   = list[i]['VIN']
#         # print("Price: ", price, "Vin: ", vin)
#         suggested = price
#         suggested = suggested.replace(',', '')
#         price = price.replace(',', '')
#         suggested = suggested.replace('$', '')
#         price = price.replace('$', '')
#         price = price.replace(' ', '')
#         # print('no', i, 'p: ',price)
        
#         try:
#             ratio = int(suggested)/int(price) #metric for rating deal
#         except: 
#             ratio == 'No Ratio'
            
#         row = (vin,ratio)
#         deals.append(row)
#         # print("Ratio: ", ratio)
    
#     # Sorted list of deals in descending order from best to worst deal
#     deals.sort(key=lambda y: -y[1])
#     # print("\ndeals: ", deals)
#     topDeals = [deals[0], deals[1], deals[2], deals[3], deals[4]]
#     return topDeals




#return top 3 cars urls from list of vins
def getTopCars(car_list, deals):
    # for i, val in enumerate(itertools.islice(deals, 2)):
    #     print(i)
    topCars = []
    for n in range(len(deals)):
        found = False
        for c in car_list:
            if found == True:
                continue
            if(c['VIN'] == deals[n][1] and c['price'] == deals[n][3]):
                topCars.append(c)
                found = True
    return topCars
    


#inprogress
def dollarValue(make, model, year, miles, zipcode):
    start = time.time()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    

    browser.get('https://www.cargurus.com/Cars/car-valuation')
    
    purposeInputList = browser.find_element(By.ID, 'carPicker_purposeSelect')
    purposeInput = Select(purposeInputList)
    purposeInput.select_by_visible_text('Buying a car')
    
    # browser.find_element_by_xpath("//select[@name='carPicker_purposeSelect']/option[text()='Buying a ca']").click()
    
    makeInputList = browser.find_element(By.ID, 'carPicker_makerSelect')
    makeInput = Select(makeInputList)
    makeInput.select_by_visible_text(make)
    
    modelInputList = browser.find_element(By.ID, 'carPicker_modelSelect')
    modelInput = Select(modelInputList)
    modelInput.select_by_visible_text(model)
    
    yearInputList = browser.find_element(By.ID, 'carPicker_year1Select')
    yearInput = Select(yearInputList)
    yearInput.select_by_visible_text(year)
    
    # trimInputList = browser.find_element(By.ID, 'carPicker_trimSelect').find_element(By.CSS_SELECTOR,"#Trims with data .eligibleTrimsGroup")
    # trimInput = Select(trimInputList)
    # trimInput.select_by_visible_text(trim)
    
    mileageInput = browser.find_element(By.NAME, 'carDescription.mileage')
    zipcodeInput = browser.find_element(By.NAME, 'carDescription.postalCode')
    
    mileageInput.send_keys(miles)
    zipcodeInput.send_keys(zipcode)
    
    while(True):
        price = browser.find_element(By.ID, 'instantMarketValuePrice').text

        if (price != "$ Calculating..."):
            print("Suggested Price from CarGurus:", price)
            end = time.time()
            print("The time of execution of above program is :",
                (end-start) * 10**3, "ms")
            return price


### Function that looks up the suggested retail value for
# the specific vehicle using the VIN passed in ###
def dollarValueVin(vin):
    start = time.time()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    browser.get('https://www.cargurus.com/Cars/car-valuation')


    # Click "Look up by VIN"
    vinButton = browser.find_element(By.ID, 'searchByVinToggle').click()

    # input vin form
    vinInput = browser.find_element(By.ID, 'carIdentifier')
    
    # input the vin 
    vinInput.send_keys(vin)

    # Click "lookup"
    lookUp = browser.find_element(By.ID, 'instantMarketValueFromVIN_0').click()

    # Ensure that the suggested price is visible
    while(True):
        idFound = False

        # To Ensure that the ID 'instantMarketValuePrice' is visible
        try:
            price = browser.find_element(By.ID, 'instantMarketValuePrice').text
            idFound = True
        except:
            print("Error finding ID instantMarketValuePrice")

        if (idFound and (price != "$ Calculating..." and price != "$—")):
            print("Suggested Price from CarGurus:", price)
            end = time.time()
            print("The time of execution of above program (VIN) is :",
                    (end-start) * 10**3, "ms")
            return price
    

### Function that looks up the suggested retail value for
# the specific vehicle using the VIN passed in ###
# version 2 takes in a dictionary of car data that holds the VIN instead of a VIN string
def dollarValueVin2(c):
    start = time.time()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    browser.get('https://www.cargurus.com/Cars/car-valuation')


    # Click "Look up by VIN"
    vinButton = browser.find_element(By.ID, 'searchByVinToggle').click()

    # input vin form
    vinInput = browser.find_element(By.ID, 'carIdentifier')
    
    # input the vin 
    vinInput.send_keys(c['VIN'])

    # Click "lookup"
    lookUp = browser.find_element(By.ID, 'instantMarketValueFromVIN_0').click()

    # Ensure that the suggested price is visible
    while(True):
        idFound = False

        # To Ensure that the ID 'instantMarketValuePrice' is visible
        try:
            price = browser.find_element(By.ID, 'instantMarketValuePrice').text
            idFound = True
        except:
            print("Error finding ID instantMarketValuePrice")

        if (idFound and (price != "$ Calculating..." and price != "$—")):
            print("Suggested Price from CarGurus:", price)
            end = time.time()
            print("The time of execution of above program (VIN) is :",
                    (end-start) * 10**3, "ms")
            return price

def dollarValueVin3(vin):
    url = "https://car-utils.p.rapidapi.com/marketvalue"

    querystring = {"vin": vin}

    headers = {
        "X-RapidAPI-Key": "eabb27e940mshbaf991f2c492656p1afbb7jsnc31638e26d33",
        "X-RapidAPI-Host": "car-utils.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)


    ### MIGHT NEED THIS ###
    # while(True):
    #     response = requests.request("GET", url, headers=headers, params=querystring)

    #     print(response.text)
    #     err = re.search('"message":', response.text)
    #     print( err )
    #     if (err):
    #         time.sleep(2)
    #         continue
    #     else:
    #         break



    
    apiResponse = response.text
    # print(response.text)
    #if no market value data
    if '"vehicle":null' in response.text:
        return "0"
    while(1):
        if 'You have exceeded the rate limit per second for your plan, BASIC, by the API provider' in response.text:
            time.sleep(1)
            response = requests.request("GET", url, headers=headers, params=querystring)
            apiResponse = response.text
        else:
            break


    start = re.search('"prices":', response.text)
    end = re.search(',"distribution"', response.text)
    
    if start is None or end is None:
        return '0'
    if start.span() is None:
        return '0'
    listOfstart = start.span()
    if end.span() is None:
        return '0'
    listOfEnd   = end.span()
    start2      = listOfstart[1]
    end2        = listOfEnd[0]


    prices = apiResponse[start2 + 1:end2]

    avg  = re.search('"average":', prices)
    avg2 = avg.span()
    avgEnd = avg2[1]

    blw = re.search('"below":', prices)
    blw2   = blw.span()
    blwStart = blw2[0]
    blwEnd = blw2[1]
    

    abv = re.search('"above":', prices)
    abv2   = abv.span()
    abvStart = abv2[0]
    abvEnd = abv2[1]

    # print("\n---------For VIN:", vin, " ---------")
    average = prices[avgEnd:blwStart - 1]
    # print("AVERAGE:", average)

    below = prices[blwEnd:abvStart - 1]
    # print("BELOW:", below)

    above = prices[abvEnd:]
    # print("ABOVE:", above, "\n\n")
    time.sleep(1)
    return below


# Car Utils with Mileage
def dollarValueVin4(vin, mileage):
    url = "https://car-utils.p.rapidapi.com/marketvalue"

    querystring = {"vin": vin, "mileage": mileage}

    headers = {
        "X-RapidAPI-Key": "eabb27e940mshbaf991f2c492656p1afbb7jsnc31638e26d33",
        "X-RapidAPI-Host": "car-utils.p.rapidapi.com"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)


    ### MIGHT NEED THIS ###
    # while(True):
    #     response = requests.request("GET", url, headers=headers, params=querystring)

    #     print(response.text)
    #     err = re.search('"message":', response.text)
    #     print( err )
    #     if (err):
    #         time.sleep(2)
    #         continue
    #     else:
    #         break



    
    apiResponse = response.text
    # print(response.text)
    #if no market value data
    if '"vehicle":null' in response.text:
        return "0"
    while(1):
        if 'You have exceeded the rate limit per second for your plan, BASIC, by the API provider' in response.text:
            time.sleep(1)
            response = requests.request("GET", url, headers=headers, params=querystring)
            apiResponse = response.text
        else:
            break
    
    if '"message":"invalid vin"' in response.text:
        return '0'

    start = re.search('"prices":', response.text)
    end = re.search(',"distribution"', response.text)
    
    if start is None or end is None:
        return '0'
    if start.span() is None:
        return '0'
    listOfstart = start.span()
    if end.span() is None:
        return '0'
    listOfEnd   = end.span()
    start2      = listOfstart[1]
    end2        = listOfEnd[0]


    prices = apiResponse[start2 + 1:end2]

    avg  = re.search('"average":', prices)
    avg2 = avg.span()
    avgEnd = avg2[1]

    blw = re.search('"below":', prices)
    blw2   = blw.span()
    blwStart = blw2[0]
    blwEnd = blw2[1]
    

    abv = re.search('"above":', prices)
    abv2   = abv.span()
    abvStart = abv2[0]
    abvEnd = abv2[1]

    print("\n---------For VIN:", vin, " ---------")
    average = prices[avgEnd:blwStart - 1]
    print("AVERAGE:", average)

    below = prices[blwEnd:abvStart - 1]
    print("BELOW:", below)

    above = prices[abvEnd:]
    print("ABOVE:", above, "\n\n")
    time.sleep(1)
    return below


# Car Utils with Mileage
def dollarValueVin4(vin, mileage):
    url = "https://car-utils.p.rapidapi.com/marketvalue"

    querystring = {"vin": vin, "mileage": mileage}

    headers = {
        "X-RapidAPI-Key": "eabb27e940mshbaf991f2c492656p1afbb7jsnc31638e26d33",
        "X-RapidAPI-Host": "car-utils.p.rapidapi.com"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)


    ### MIGHT NEED THIS ###
    # while(True):
    #     response = requests.request("GET", url, headers=headers, params=querystring)

    #     print(response.text)
    #     err = re.search('"message":', response.text)
    #     print( err )
    #     if (err):
    #         time.sleep(2)
    #         continue
    #     else:
    #         break



    
    apiResponse = response.text
    # print(response.text)
    #if no market value data
    if '"vehicle":null' in response.text:
        return "0"
    while(1):
        if 'You have exceeded the rate limit per second for your plan, BASIC, by the API provider' in response.text:
            time.sleep(1)
            response = requests.request("GET", url, headers=headers, params=querystring)
            apiResponse = response.text
        else:
            break
    
    if '"message":"invalid vin"' in response.text:
        return '0'

    start = re.search('"prices":', response.text)
    end = re.search(',"distribution"', response.text)
    
    if start is None or end is None:
        return '0'
    if start.span() is None:
        return '0'
    listOfstart = start.span()
    if end.span() is None:
        return '0'
    listOfEnd   = end.span()
    start2      = listOfstart[1]
    end2        = listOfEnd[0]


    prices = apiResponse[start2 + 1:end2]

    avg  = re.search('"average":', prices)
    avg2 = avg.span()
    avgEnd = avg2[1]

    blw = re.search('"below":', prices)
    blw2   = blw.span()
    blwStart = blw2[0]
    blwEnd = blw2[1]
    

    abv = re.search('"above":', prices)
    abv2   = abv.span()
    abvStart = abv2[0]
    abvEnd = abv2[1]

    # print("\n---------For VIN:", vin, " ---------")
    average = prices[avgEnd:blwStart - 1]
    # print("AVERAGE:", average)

    below = prices[blwEnd:abvStart - 1]
    # print("BELOW:", below)

    above = prices[abvEnd:]
    # print("ABOVE:", above, "\n\n")
    time.sleep(1)
    return below

if __name__ == '__main__':
    main()