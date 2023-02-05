import cheerio from 'cheerio';
import axios from 'axios';
import webdriver from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';
import chromedriver from 'chromedriver';


// URL of the page to scrape
var url = 'https://www.cars.com/vehicledetail/68e47606-5598-41ad-b60d-97c8a10e6b75/';
var url2 = 'https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=666054295&allListingType=all-cars&zip=20001&makeCodeList=ROV&modelCodeList=RANGE&state=DC&city=Washington&searchRadius=50&isNewSearch=false&referrer=%2Fcars-for-sale%2Fall-cars%3Fzip%3D20001%26makeCodeList%3DROV%26modelCodeList%3DRANGE&clickType=spotlight';
var url3 = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=d116&zip=20001#listing=311628708/FEATURED'


//cars.com
async function singleCarData1(url) {
    axios.get(url)
    .then((response) => {
        // Load the HTML into cheerio
        var $ = cheerio.load(response.data);

        // Select the element that contains the data we want to scrape
        // In this example, we want to scrape the title of the car
        var title = $('h1.listing-title').text();

        // Split the title into its parts (year, make, model, trim)
        var titleParts = title.split(' ');

        // Extract the year, make, model, and trim from the title
        var zip = 20001
        var year = titleParts[0];
        var make = titleParts[1];

        //special case for tesla:
        if (make.toLowerCase() == 'tesla'){
            if (model.toLowerCase().replace(' ', '') == 'model'){
                model = titleParts[2] + ' ' + titleParts[3]
            }
            return
        } //special case for land rover:
        else if (make.toLowerCase() == 'land'){
            make = 'Land Rover'
            model = titleParts[3]
            if (model.toLowerCase() == 'range'){
                model = 'Range Rover'
            }
            return
        }
        
        var model = titleParts[2];
        var trim = titleParts[3];

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
        console.log(`Trim: ${trim}`);
    })
    .catch((error) => {
        console.error(error);
    });
}

//autotrader
async function singleCarData2(url) {
    axios.get(url)
    .then((response) => {
        // Load the HTML into cheerio
        var $ = cheerio.load(response.data);
        // Select the element that contains the data we want to scrape
        // In this example, we want to scrape the title of the car
        var title = $('h1[class="text-bold text-size-400 text-size-sm-700 col-xs-12 col-sm-7 col-md-8"]').text();

        // Split the title into its parts (year, make, model, trim)
        var titleParts = title.split(' ');
        var zip = 20001
        // Extract the year, make, model, and trim from the title
        var year = titleParts[1];
        var make = titleParts[2];
        
        //special case for tesla:
        if (make.toLowerCase() == 'tesla'){
            if (model.toLowerCase().replace(' ', '') == 'model'){
                model = titleParts[3] + ' ' + titleParts[4]
            }
            return
        } //special case for land rover:
        else if (make.toLowerCase() == 'land'){
            make = 'Land Rover'
            model = titleParts[4]
            if (model.toLowerCase() == 'range'){
                model = 'Range Rover'
            }
            console.log(`Year: ${year}`);
            console.log(`Make: ${make}`);
            console.log(`Model: ${model}`);
            return
        }

        var model = titleParts[3];
        var trim = titleParts[4]
        // var trim = (rawTrim.split('w/'))[0];

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
    })
    .catch((error) => {
        console.error(error);
    });
}

//cargurus
async function singleCarData3(url) {

    // Create a new webdriver instance
    const driver = new webdriver.Builder()
    .forBrowser('chrome')
    .build();

    // Use the webdriver instance to navigate to the website you want to scrape
    driver.get(url);

    // Get the HTML content of the page
    var html = await driver.getPageSource();
    console.log(html);
    // Load the HTML content into cheerio
    const $ = cheerio.load(html);

    // Select the element that contains the data we want to scrape
    // In this example, we want to scrape the title of the car
    var title = $('h1[class="IpF2YF"]').text();
    console.log(title)
    if(title == null){
        console.log('page err 1')
        return
    }
    // Split the title into its parts (year, make, model, trim)
    var titleParts = title.split(' ');
    var zip = 20001
    // Extract the year, make, model, and trim from the title
    var year = titleParts[0];
    var make = titleParts[1];
    if(titleParts[2] == null){
        console.log(title)
        console.log('page err 2')
        return
    }
    
    //special case for tesla:
    if (make.toLowerCase() == 'tesla'){
        if (model.toLowerCase().replace(' ', '') == 'model'){
            model = titleParts[2] + ' ' + titleParts[3]
        }
        return
    } //special case for land rover:
    else if (make.toLowerCase() == 'land'){
        make = 'Land Rover'
        model = titleParts[3]
        if (model.toLowerCase() == 'range'){
            model = 'Range Rover'
        }
        return
    }

    var model = titleParts[2];
    var trim = titleParts[3];
    

    // Print the scraped data
    console.log(`Year: ${year}`);
    console.log(`Make: ${make}`);
    console.log(`Model: ${model}`);
    console.log(`Trim: ${trim}`);

    // Close the webdriver
    driver.close();
}

//edmunds
async function singleCarData4(url) {
    axios.get(url)
    .then((response) => {
        // Load the HTML into cheerio
        var $ = cheerio.load(response.data);

        // Select the element that contains the data we want to scrape
        // In this example, we want to scrape the title of the car
        var title = $('h1[class="not-opaque text-black d-inline-block mb-0 size-24"]').text();

        // Split the title into its parts (year, make, model, trim)
        var titleParts = title.split(' ');
        var zip = 20001
        // Extract the year, make, model, and trim from the title
        var year = titleParts[0];
        var make = titleParts[1];
        
        //special case for tesla:
        if (make.toLowerCase() == 'tesla'){
            if (model.toLowerCase().replace(' ', '') == 'model'){
                model = titleParts[2] + ' ' + titleParts[3]
            }
            console.log(`Year: ${year}`);
            console.log(`Make: ${make}`);
            console.log(`Model: ${model}`);
            return
        } //special case for land rover:
        else if (make.toLowerCase() == 'land'){
            make = 'Land Rover'
            model = titleParts[3]
            if (model.toLowerCase() == 'range'){
                model = 'Range Rover'
            }
            console.log(`Year: ${year}`);
            console.log(`Make: ${make}`);
            console.log(`Model: ${model}`);
            return
        }
        var model = titleParts[2];
        

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
        console.log(`Trim: ${trim}`);
    })
    .catch((error) => {
        console.error(error);
    });
}

//carsdirect
async function singleCarData5(url) {
    axios.get(url)
    .then((response) => {
        // Load the HTML into cheerio
        var $ = cheerio.load(response.data);

        // Select the element that contains the data we want to scrape
        // In this example, we want to scrape the title of the car
        var title = $('h1[class="top-bar-title-set"]').text();

        // Split the title into its parts (year, make, model, trim)
        var titleParts = title.split(' ');
        var zip = 20001
        // Extract the year, make, model, and trim from the title
        var year = titleParts[0];
        var make = titleParts[1];

        
        //special case for tesla:
        if (make.toLowerCase() == 'tesla'){
            if (model.toLowerCase().replace(' ', '') == 'model'){
                model = titleParts[2] + ' ' + titleParts[3]
            }
            return
        } //special case for land rover:
        else if (make.toLowerCase() == 'land'){
            make = 'Land Rover'
            model = titleParts[3]
            if (model.toLowerCase() == 'range'){
                model = 'Range Rover'
            }
            return
        }

        var model = titleParts[2];
        

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
        console.log(`Trim: ${trim}`);
    })
    .catch((error) => {
        console.error(error);
    });
}

// singleCarData4('https://www.edmunds.com/land-rover/range-rover/2019/vin/SALGS2RE8KA543850/?radius=50')
singleCarData5('https://www.carsdirect.com/used_cars/vehicle-detail/ul2169875111/ford/bronco?source=UsedCarListings&savedVehicleId=&recentSearchId=13263876')