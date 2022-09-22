import scrapeV1
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#incomplete
def Rate(make, model, year, zipcode):
    list = scrapeV1.ScrapeToList(make, model, year, zipcode)
    # with open('cardata.csv', 'r', encoding='utf8', newline='') as f:
    #     reader = csv.reader(f)
    #     cars = []
    #     for row in reader:
    #         list_item = row.split(',', 4)
    #         cars.append(list_item)
    #         print(list_item[1])
    for c in list:
        print(c[3])

#inprogress
def DollarValue():
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    browser.get('https://www.cargurus.com/Cars/car-valuation')
    
    purposeInputList = browser.find_element(By.ID, 'carPicker_purposeSelect')
    purposeInput = Select(purposeInputList)
    purposeInput.select_by_visible_text('Buying a car')
    
    # browser.find_element_by_xpath("//select[@name='carPicker_purposeSelect']/option[text()='Buying a ca']").click()

    
    makeInputList = browser.find_element(By.ID, 'carPicker_makerSelect')
    makeInput = Select(makeInputList)
    makeInput.select_by_visible_text('Ford')
    
    modelInputList = browser.find_element(By.ID, 'carPicker_modelSelect')
    modelInput = Select(modelInputList)
    modelInput.select_by_visible_text('Mustang')
    
    yearInputList = browser.find_element(By.ID, 'carPicker_year1Select')
    yearInput = Select(yearInputList)
    yearInput.select_by_visible_text('2001')
    
    trimInputList = browser.find_element(By.ID, 'carPicker_trimSelect').find_element(By.CSS_SELECTOR,"#Trims with data .eligibleTrimsGroup")
    trimInput = Select(trimInputList)
    trimInput.select_by_visible_text('Premium Convertible RWD')
    
    mileageInput = browser.find_element(By.NAME, 'carDescription.mileage')
    zipcodeInput = browser.find_element(By.NAME, 'carDescription.postalCode')
    
    mileageInput.send_keys('120000')
    zipcodeInput.send_keys('22201')
    
    price = browser.find_element(By.ID, 'instantMarketValuePrice').getText()
    print(price)

    
# DollarValue()     

    
