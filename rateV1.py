import csv
import time
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

carlist = []

carlist = []

def main():

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
 
 
    #getTopCars test
    # deals = [('WBA1G9C51GV599609', 7.357627118644068), ('WBA73AK03M7H21242', 0.9995336076817558), ('WBA1G9C51GV599609', 0.869939879759519), ('WBA1F5C50EV255231', 0.700531208499336), ('WBA73AK03M7H21242', 0.45286513362336855), ('WBA1F5C50EV255231', 0.3009127210496292)]
    # deals = rate(createList())
    list = createList()
    deals = [('ZHWUC1ZD4ELA02158', 1.1615157732751988), ('ZHWUC1ZD0ELA02996', 1.0945740025740025), ('ZHWUC1ZD6ELA02419', 1.0391110222217417), ('ZHWUC1ZD0CLA00114', 0.9697389581524244), ('ZHWUG4ZD2HLA06039', 0.9664653979314289), ('ZHWUF3ZD8GLA04324', 0.5678466881216022), ('ZHWUR1ZD5ELA02331', 0.48796481503795636), ('ZHWUC1ZD0FLA03633', 0.48796481503795636), ('ZHWUR1ZD9FLA03502', 0.21584448056007)]
    print(getTopCars(list, rate(list)))
 
    # listOfCars = createList()
    # print(listOfCars)
    # dollarValueVin('ZHWUC1ZD4ELA02158')

    




def createList():
    csv_filename = 'cardata.csv'
    # carlist =[]
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            carlist.append(row)
    # print("Done")

    # for i in range(len(carlist)):
    #     print("|",carlist[i]['Price'],"|")
    #     # print(carlist[i])
    
    return carlist

#incomplete
def rate(list):
    # carlist = createList()

    deals = []
    for i in range(len(list)):
        price = list[i]['Price']
        vin   = list[i]['VIN']
        print("Price: ", price, "Vin: ", vin)
        suggested = dollarValueVin(vin)
        suggested = suggested.replace(',', '')
        price = price.replace(',', '')
        suggested = suggested.replace('$', '')
        price = price.replace('$', '')
        price = price.replace(' ', '')
        # print('no', i, 'p: ',price)
        
        try:
            ratio = int(suggested)/int(price) #metric for rating deal
        except: 
            ratio == 'No Ratio'
            
        row = (vin,ratio)
        deals.append(row)
        print("Ratio: ", ratio)
    
    # Sorted list of deals in descending order from best to worst deal
    deals.sort(key=lambda y: -y[1])
    print("\ndeals: ", deals)
    topDeals = [deals[0], deals[1], deals[2]]
    return topDeals

#return top 3 cars urls from list of vins
def getTopCars(car_list, deals):
    # for i, val in enumerate(itertools.islice(deals, 2)):
    #     print(i)
    topCars = []
    for c in car_list:
        if(c['VIN'] == deals[0][0]):
            print(c['VIN'])
            print(deals[0])
            topCars.append(c)
    for c in car_list:
        if(c['VIN'] == deals[1][0]):
            print(c['url'])
            topCars.append(c)
    for c in car_list:
        if(c['VIN'] == deals[2][0]):
            print(c['url'])
            topCars.append(c)
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

if __name__ == '__main__':
    main()