import $ from "jquery";
import axios from 'axios';
import cheerio from 'cheerio';

async function singleCarData1(url) {
    const singleCarData = await axios.get(url)
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
            return {year, make, model, trim}
        } //special case for land rover:
        else if (make.toLowerCase() == 'land'){
            make = 'Land Rover'
            model = titleParts[3]
            if (model.toLowerCase() == 'range'){
                model = 'Range Rover'
            }
            return {year, make, model, trim}
        }
        
        var model = titleParts[2];
        var trim = titleParts[3];

        const vinRegex = /[A-HJ-NPR-Z\d]{17}/g;
        // search for VIN numbers in Cheerio HTML variable
        const vinNumbers = $('body').text().match(vinRegex);
        var VIN = vinNumbers[0]
        var imgURL = $('gallery-slides img').attr('src');
        var price = $('div.price-section span').first().text().replace('$', '').replace(',', '')
        var mileage = $('div.listing-mileage').text().replace(' mi.', '').replace(',', '').replace(' ', '')
        

        // console.log('single car data response:', make)
        return {year, make, model, trim, VIN, imgURL, mileage, price, url}
    })
    .catch((error) => {
        console.error(error);
    });

    // setTimeout(5000); // wait for 1 second (1000 milliseconds)
    // var postData = JSON.stringify(await singleCarData)
    //     const config = {
    //         headers: {
    //           'Content-Type': 'application/json;charset=utf-8'
    //         }
    //       };

    // axios.post('http://localhost:8080/addCurrent', postData, config)
    //     .then(response => {
    //         console.log(response);
    //     })
    //     .catch(error => {
    //         console.error(error);
    //     });
    return singleCarData
}

async function singleCarData2(url) {
    const carData = await axios.get(url)
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
            return {year, make, model, trim}
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
            return {year, make, model, trim}
        }

        var model = titleParts[3];
        var trim = titleParts[4]
        // var trim = (rawTrim.split('w/'))[0];
        const vinRegex = /[A-HJ-NPR-Z\d]{17}/g;
        // search for VIN numbers in Cheerio HTML variable
        const vinNumbers = $('body').match(vinRegex)
        var VIN = vinNumbers[0]

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
        console.log(`Trim: ${trim}`);
        console.log(`VIN regex: ${vinNumbers}`)

        return {year, make, model, trim}
    })
    .catch((error) => {
        console.error(error);
    });
}

console.log(await singleCarData2('https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=674949882&allListingType=all-cars&zip=20001&makeCodeList=DODGE&modelCodeList=DURANG&state=DC&city=Washington&searchRadius=50&isNewSearch=false&referrer=%2Fcars-for-sale%2Fall-cars%3Fzip%3D20001%26makeCodeList%3DDODGE%26modelCodeList%3DDURANG&clickType=spotlight'))
