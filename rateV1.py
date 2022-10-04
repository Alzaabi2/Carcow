import scrapeV1
import scrapeV1_1
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


carlist = []

def createList():
    csv_filename = 'cardata.csv'
    # carlist =[]
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print(row)
            # print(row['Make'])
            carlist.append(row)

    # print(carlist[5]["Price"])
    # print(carlist[5])

    for i in range(len(carlist)):
        # print("|",carlist[i]['Price'],"|")
        if carlist[i]['Price'] == ' Not Priced ':
            carlist.remove(i)
    
#incomplete
def rate(make, model, year, zipcode):
    # list = scrapeV1.ScrapeToList(make, model, year, zipcode)
    scrapeV1.Scrape(make,model,year,zipcode)
    createList()
    


    # for c in list:
    #     print("Make:", c[0], ",Model:", c[1], ",Year:", c[2], ",Mileage:", c[3], ",Price:", c[4])


    # with open('cardata.csv', 'r', encoding='utf8', newline='') as f:
    #     reader = csv.reader(f)
    #     cars = []
    #     for row in reader:
    #         list_item = row.split(',', 4)
    #         cars.append(list_item)
    #         print(list_item[1])
    # for c in list:
        # print("Make:", c[0], ",Model:", c[1], ",Year:", c[2], ",Mileage:", c[3], ",Price:", c[4])


#inprogress
def dollarValue(make, model, year, trim, miles, zipcode):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    

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
    
    trimInputList = browser.find_element(By.ID, 'carPicker_trimSelect').find_element(By.CSS_SELECTOR,"#Trims with data .eligibleTrimsGroup")
    trimInput = Select(trimInputList)
    trimInput.select_by_visible_text(trim)
    
    mileageInput = browser.find_element(By.NAME, 'carDescription.mileage')
    zipcodeInput = browser.find_element(By.NAME, 'carDescription.postalCode')
    
    mileageInput.send_keys(miles)
    zipcodeInput.send_keys(zipcode)
    
    while(True):
        price = browser.find_element(By.ID, 'instantMarketValuePrice').text

        if (price != "$ Calculating..."):
            print("Suggested Price from CarGurus:", price)
            return price


### Function that looks up the suggested retail value for
# the specific vehicle using the VIN passed in ###
def dollarValueVin(vin):
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
        price = browser.find_element(By.ID, 'instantMarketValuePrice').text

        if (price != "$ Calculating..."):
            print("Suggested Price from CarGurus:", price)
            return price
    

# dollarValue('Mercedes-Benz', 'S-class', '2007', 130065, 22701) # Need to know which car from chrome extension

dollarValueVin('WBA73AK06M7H36558')
# rate('Audi', 'A3', '2017', '22182')

# createList()