import mysql.connector 
from rateV1 import *
from scrapeV1_6_database_mass_search import *



mydb = mysql.connector.connect(
    host="carcow.ce0uqlnzw4og.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Hevcy4-gumden-wypjav",
    database="CarCowDB"
)

def populateScraped(list):
    cursor = mydb.cursor(buffered=True,dictionary=True)

    # list = createList()
    if len(list) == 0 or list is None:
        print("List is empty")
        return

    for i in list:
        if i['VIN'] is None:
            continue
        else:
            vin   = i['VIN']
        make  = i['Make']
        model = i['Model']
        trim  = i['Trim']
        # trim = ''
        year  = i['Year'].replace(' ', '')
        year2 = re.findall(r'\d+\d+', year)
        if len(year2) == 0:
            year2.append('-1')

        mileage = i['Mileage']
        mileage2 = mileage.replace(',','')
        miles = re.findall(r'\d+\d+', mileage2)
        if len(miles) == 0:
            miles.append('-1')
            
        price2  = i['Price'].replace('$','').replace(' ','').replace(',', '')
        # print(price2)
        # try:
        #     price = float(price)
        #     price = str(price)
        # except:
        #     price = 'invalid'
        # re.findall(r'\d+\d+', mileage2)
        if len(price2) == 0:
            price2.append('-1')

        url   = i['url']

        imageurl = i['img']
        # imageurl = ''
        
        cmd = "SELECT VIN from scraped WHERE VIN = '" + vin+"'"
        # print(cmd)
        cursor.execute(cmd)
        result = cursor.fetchall()
        if len(result) != 0:
            continue
        
        suggested = dollarValueVin4(vin, int(miles[0]))

        # print("Model:", model)
        # print("Trim:", trim)
        
        # try:

        # print("Inserting text:  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (vin, make, model, year2[0], trim, miles[0], price2, suggested, url, imageurl))
        # print(str(vin, make, model, year2[0], trim, miles[0], price2, suggested, url, imageurl))
        cursor.execute("INSERT INTO scraped (VIN, make, model, year, trim, mileage, price, suggested, url, imageurl, date)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (vin, make, model, year2[0], trim, miles[0], price2, suggested, url, imageurl))

        mydb.commit()
        # print('its in')
        # except:
        #     print('entry error')
    print('inserted : '+ str(len(list)))
    print('example vin: '+ list[0]['VIN'])

    # # get vin, make, model, and trim of cars stored within the last 30 days
    # cursor.execute("SELECT VIN,make,model,trim FROM scraped WHERE DATE_SUB(CURDATE(),INTERVAL 30 DAY) <= DATE(date)")
    # test = cursor.fetchall()
    # print(test)



# list = Scrape1('Fiat')
# print(list)
# populateScraped(list)



