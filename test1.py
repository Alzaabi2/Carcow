from extension import *
from scrapeV1_6 import *
import json
import urllib
import requests
import random
import csv

def getMakeModel():
    filename = 'makemodel.json'
    carlist = []
    with open(filename) as f:
        # reader = csv.DictReader(f)
        # for row in reader:
        #     carlist.append(row)
        data = json.load(f)
        for i in data['results']:
            entry = {'Make': i['Make'], 'Model': i['Model'], 'Year':str(i['Year'])}
            carlist.append(entry)
            # print(entry)
    return carlist
    

def scrapeTest():
    print('Scrape Test 1 :')
    list = getMakeModel()
    r = random.random()
    r = round(r * 100)
    zip = 22201
    for i in list:
        # zip = zip + 300
        print(' ')
        print('Scraping: ['+i['Make']+', '+i['Model']+', '+i['Year']+', '+str(zip)+']')
        try:
            ScrapeAlpha(i['Make'], i['Model'], i['Year'], str(zip))
        except:
            print('Error')

    return


# singleCar ={"Make": "Ford", "Model": "Challenger", "Year":"200"}

# tempData = [{"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"},  {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": "3,030 miles", "Price": "$30,998", "VIN": "2C3CDZAG5NH212014", "url": "https://www.edmunds.com/dodge/challenger/2022/vin/2C3CDZAG5NH212014/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2022", "Mileage": " 2,512 miles ", "Price": "$32,590 ", "VIN": "2C3CDZAG2NH140284", "url": "/used_cars/vehicle-detail/ul2152699317/dodge/challenger"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}, {"Make": "Dodge", "Model": "Challenger", "Year": "2016", "Mileage": "140,403 miles", "Price": "$13,950", "VIN": "2C3CDZAG7GH352696", "url": "https://www.edmunds.com/dodge/challenger/2016/vin/2C3CDZAG7GH352696/?radius=50"}]

# with open('TempData.txt', 'w', encoding='utf8', newline='\n') as f:
#         w = writer(f)
#         header = ['Make', 'Model', 'Year', 'Mileage', 'Price', 'VIN', 'url']
#         w.writerow(header)
#         for i in range(len(tempData)):
#             row = [tempData[i]['Make'], tempData[i]['Model'], tempData[i]['Year'], tempData[i]['Mileage'], tempData[i]['Price'], tempData[i]['VIN'], tempData[i]['url']]
#             w.writerow(row)
            
#         # f.write(json.dumps(singleCar))
#         # f.write('\n')
#         # for i in topCars:
#         #     f.write(json.dumps(topCars))
#         #     f.write(i)
#         #     f.write('\n')



# with open('TempData.txt', 'r') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         tempData.append(row)

# print(tempData[3]['Year'])

# list =
deals = [('3C3CFFARXGT205497', 1.3583396310291176, '$8,998'), ('3C3CFFFH1DT620168', 1.2934765032844873, '9,895'), ('3C3CFFFH7DT744638', 1.2863266331658292, '$9,950'), ('3C3CFFDR4DT514860', 1.1755422626788037, '$7,690'), ('3C3CFFJH4DT635982', 1.164599636032757, '10,990'), ('3C3CFFJH4DT635982', 1.164599636032757, '$10,990'), ('3C3CFFFH5DT573808', 1.1640700318326513, '10,995'), ('3C3CFFFH5DT573808', 1.1640700318326513, '$10,995'), ('3C3CFFFH3DT608684', 1.1640700318326513, '$10,995'), ('3C3CFFAR1DT545813', 1.1383114285714286, '7,000'), ('3C3CFFAR1DT545813', 1.1383114285714286, '$7,000'), ('3C3CFFDR8DT636010', 1.130131266408301, '7,999'), ('3C3CFFDR8DT636010', 1.130131266408301, '$7,999'), ('3C3CFFAR8FT504453', 1.1040322763950448, '$8,799'), ('3C3CFFHH4FT504396', 1.0452528651991997, '$10,994'), ('3C3CFFBR6FT753820', 1.0446827272727273, '$11,000'), ('3C3CFFKRXHT586378', 1.0412830593280915, '$13,990 '), ('3C3CFFDR0DT624563', 1.027847640704946, '$8,795'), ('3C3CFFAR1DT740052', 1.0086303797468354, '$7,900'), ('3C3CFFFH4FT570644', 1.00285949280329, '$14,590 '), ('3C3CFFAR0DT750572', 0.9967700775581687, '7,994'), ('3C3CFFAR0DT750572', 0.9967700775581687, '$7,994'), ('3C3CFFAR1CT112717', 0.9962923274753537, '$6,999'), ('3C3CFFCH6JT524097', 0.9920205669816565, '$17,990'), ('3C3CFFFH8FT741590', 0.9760987324883255, '$14,990 '), ('3C3CFFKH9JT528713', 0.9693466745144202, '$16,990 '), ('3C3CFFJH6HT643734', 0.92936450630709, '$22,990'), ('3C3CFFCR5DT749561', 0.929218, '10,000'), ('3C3CFFCR5DT749561', 0.929218, '$10,000'), ('3C3CFFKH8JT511529', 0.9154641467481934, '$17,990 '), ('3C3CFFKH9JT377808', 0.9150572285809535, '$17,998'), ('3C3CFFFH5FT550144', 0.9150544090056285, '$15,990 '), ('3C3CFFFH1DT528364', 0.9148641887062188, '13,990'), ('3C3CFFJH0DT743922', 0.9148641887062188, '13,990'), ('3C3CFFFH1DT528364', 0.9148641887062188, '$13,990 '), ('3C3CFFJH5DT693289', 0.9148641887062188, '$13,990 '), ('3C3CFFFH6DT648709', 0.9148641887062188, '$13,990 '), ('3C3CFFJH0DT743922', 0.9148641887062188, '$13,990 '), ('3C3CFFBR4FT648421', 0.9127490071485306, '$12,590 '), ('3C3CFFKR1HT557920', 0.9110412757973733, '$15,990'), ('3C3CFFKR5HT700187', 0.9110412757973733, '$15,990'), ('3C3CFFKR7HT586497', 0.9110412757973733, '$15,990 '), ('3C3CFFKR5HT700187', 0.9110412757973733, '$15,990 '), ('3C3CFFKR0HT565765', 0.9110412757973733, '$15,990 '), ('3C3CFFKR3HT700432', 0.9110412757973733, '$15,990 '), ('3C3CFFCH0JT425744', 0.9109979581419092, '$19,590'), ('3C3CFFCH0JT425744', 0.9109979581419092, '$19,590 '), ('3C3CFFKH4JT425781', 0.8859171597633136, '$18,590 '), ('3C3CFFBR8FT721760', 0.8846428021555043, '$12,990 '), ('3C3CFFBR0CT115719', 0.8831811061573684, '$8,299'), ('3C3CFFFHXDT514091', 0.8772412611377657, '$14,590'), ('3C3CFFFHXDT514091', 0.8772412611377657, '$14,590 '), ('3C3CFFAR7GT222225', 0.8736483202287348, '$13,990 '), ('3C3CFFKH8JT503527', 0.8672564507635598, '$18,990 '), ('3C3CFFCR4FT652385', 0.8660801796023092, '$15,590 '), ('3C3CFFFH1FT521112', 0.8611959976456739, '$16,990 '), ('3C3CFFBR1ET252834', 0.8602544087886673, '$10,377'), ('3C3CFFKR8HT527765', 0.8574190700412007, '$16,990 '), ('3C3CFFFHXDT697458', 0.8538325550366912, '14,990'), ('3C3CFFFH4DT573895', 0.8538325550366912, '$14,990 '), ('3C3CFFFH6DT743450', 0.8538325550366912, '$14,990 '), ('3C3CFFFH9HT542390', 0.8493506252894859, '$21,590 '), ('3C3CFFFH7GT152631', 0.8454412206103051, '$19,990 '), ('3C3CFFFH6CT360025', 0.8431837026447462, '$13,990 '), ('3C3CFFAR1DT743680', 0.8396396206533193, '$9,490'), ('3C3CFFLR5HT571057', 0.8324660490577955, '$18,998'), ('3C3CFFFHXFT598688', 0.831820352472996, '$17,590 '), ('3C3CFFJH6DT646532', 0.8260051629557922, '15,495'), ('3C3CFFBR4FT696162', 0.82140886347391, '$13,990 '), ('3C3CFFBR1FT550494', 0.82140886347391, '$13,990 '), ('3C3CFFBR3FT741432', 0.82140886347391, '$13,990 '), ('3C3CFFBR3FT501247', 0.82140886347391, '$13,990 '), ('3C3CFFAR2GT143139', 0.8153662441627751, '$14,990 '), ('3C3CFFER8CT189014', 0.812568440200091, '$10,995'), ('3C3CFFKR2HT588383', 0.8097581989994441, '$17,990 '), ('3C3CFFAR9DT534770', 0.8089522842639594, '9,850'), ('3C3CFFCR3FT576285', 0.7947139493819895, '$16,990'), ('3C3CFFCR3FT576285', 0.7947139493819895, '$16,990 '), ('3C3CFFFH5ET276118', 0.7932382739212007, '$15,990 '), ('3C3CFFFH6CT365595', 0.7869339559706471, '$14,990 '), ('3C3CFFAR2FT598667', 0.7715949166004765, '$12,590 '), ('3C3CFFFH0DT727731', 0.7714858348402652, '16,590'), ('3C3CFFFH0DT727731', 0.7714858348402652, '$16,590 '), ('3C3CFFJH6DT628838', 0.7714858348402652, '$16,590 '), ('3C3CFFFHXFT513994', 0.7704960505529226, '$18,990 '), ('3C3CFFBRXFT607890', 0.7666117411607739, '$14,990 '), ('3C3CFFKH6JT425667', 0.7628161185734137, '$21,590 '), ('3C3CFFFH4DT686486', 0.7533225426721601, '$16,990 '), ('3C3CFFFH6DT573445', 0.7533225426721601, '$16,990 '), ('3C3CFFFH4DT551654', 0.7533225426721601, '$16,990 '), ('3C3CFFAR2FT523287', 0.7418388697976326, '$13,095'), ('3C3CFFAR9GT193472', 0.7367293550331525, '$16,590 '), ('3C3CFFBR2FT545255', 0.7186685428392746, '$15,990 '), ('3C3CFFFHXDT512082', 0.7114480266814898, '$17,990'), ('3C3CFFFHXDT512082', 0.7114480266814898, '$17,990 '), ('3C3CFFER5CT202009', 0.7096258935663226, '$12,590 '), ('3C3CFFER7CT208720', 0.7096258935663226, '$12,590 '), ('3C3CFFAR0ET264202', 0.6961331793687452, '$12,990'), ('3C3CFFAR7FT750202', 0.6943802716225875, '$13,990'), ('3C3CFFAR9FT619840', 0.6943802716225875, '$13,990'), ('3C3CFFAR7FT750202', 0.6943802716225875, '$13,990 '), ('3C3CFFAR9FT619840', 0.6943802716225875, '$13,990 '), ('3C3CFFFH0CT363258', 0.6942989994114185, '$16,990 '), ('3C3CFFFH9CT316648', 0.6942989994114185, '$16,990 '), ('3C3CFFCR6CT195137', 0.6929982743744608, '$11,590 '), ('3C3CFFBR5FT625150', 0.692676913803496, '$16,590 '), ('3C3CFFGE8DT740280', 0.6886194690265487, '12,995'), ('3C3CFFJH0DT689845', 0.6884857450242066, '$18,590 '), ('3C3CFFFH8DT553522', 0.6884857450242066, '$18,590 '), ('3C3CFFHH3DT633937', 0.6825003971405877, '$12,590 '), ('3C3CFFHH0FT507554', 0.6763690406121248, '$16,990 '), ('3C3CFFBRXFT562434', 0.6763690406121248, '$16,990 '), ('3C3CFFBR6CT110041', 0.666926296633303, '$10,990 '), ('3C3CFFAR6FT527956', 0.6658245373543522, '$14,590'), ('3C3CFFAR6FT527956', 0.6658245373543522, '$14,590 '), ('3C3CFFAR7DT514582', 0.6645688073394496, '$11,990 '), ('3C3CFFBR8DT591976', 0.6614842186297152, '$12,990 '), ('3C3CFFBR8DT737387', 0.6614842186297152, '$12,990 '), ('3C3CFFFH0CT340126', 0.6557053918843802, '$17,990 '), ('3C3CFFAR3ET208738', 0.64637383845604, '$13,990 '), ('3C3CFFBR4FT508174', 0.6387720956086715, '$17,990 '), ('3C3CFFAR5DT753953', 0.6328975377283559, '12,590'), ('3C3CFFAR5DT753953', 0.6328975377283559, '$12,590 '), ('3C3CFFAR6FT528251', 0.6231161000641436, '$15,590 '), ('3C3CFFCRXCT108078', 0.6180723355136591, '$12,995'), ('3C3CFFCR0FT582139', 0.6140150068212824, '$21,990 '), ('3C3CFFBR5DT665984', 0.6138505500785827, '$13,998'), ('3C3CFFER9CT316627', 0.6123502398903359, '$14,590 '), ('3C3CFFAR5FT536986', 0.6075284552845528, '$15,990 '), ('3C3CFFAR7ET293972', 0.6029317242298974, '$14,998'), ('3C3CFFAR3CT344056', 0.6016436583261432, '$11,590'), ('3C3CFFAR3CT344056', 0.6016436583261432, '$11,590 '), ('3C3CFFDR6CT203591', 0.5960171551107935, '$13,990 '), ('3C3CFFJH4DT672238', 0.5928184344603984, '21,590'), ('3C3CFFJH4DT672238', 0.5928184344603984, '$21,590 '), ('3C3CFFCR0CT340348', 0.5910117733627668, '$13,590 '), ('3C3CFFBR4CT102813', 0.5821699761715647, '$12,590 '), ('3C3CFFJH5DT645324', 0.5820350159163257, '$21,990 '), ('3C3CFFER7CT140029', 0.573071840923669, '$15,590 '), ('3C3CFFDR7CT355072', 0.5715065113091159, '$14,590 '), ('3C3CFFAR9DT684443', 0.5695625446747677, '$13,990 '), ('3C3CFFAR4CT313768', 0.5538562351072279, '$12,590 '), ('3C3CFFAR5DT740166', 0.5458031372011782, '$14,599'), ('3C3CFFERXCT173106', 0.538528631705847, '$16,590 '), ('3C3CFFBR8ET176903', 0.5380867992766727, '$16,590'), ('3C3CFFHH8DT554179', 0.5373783614759224, '$15,990 '), ('3C3CFFBR4CT280558', 0.45838148843026894, '$15,990 ')]

def getTopCars(car_list, deals):
    # for i, val in enumerate(itertools.islice(deals, 2)):
    #     print(i)
    topCars = []
    for n in range(len(deals)):
        found = False
        for c in car_list:
            if found == True:
                continue
            if(c['VIN'] == deals[n][0] and c['Price'] == deals[n][2]):
                topCars.append(c)
                found = True
    return topCars

