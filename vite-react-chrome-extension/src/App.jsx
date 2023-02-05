import React, { useEffect, useState, useRef } from 'react';
import './App.css';
import $, { data } from "jquery";
import axios from 'axios';
import ReactLoading from "react-loading";
import cheerio from 'cheerio';

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

function App() {
    const [urlCall, setUrl] = useState('');
    const [validWebsite, setValidWebsite] = useState('');

    const [error, setError] = useState(undefined); //Changed from useState(null)
    const [carData, setCarData] = useState(null);
    const [done, setDone] = useState(undefined);
    /*
     * Get current URL
     */
    const conditions = ['cars.com/vehicledetail', 'autotrader.com/cars-for-sale/vehicledetails', 'cargurus.com/Cars/inventorylisting/', 'edmunds.com', 'carsdirect.com/used_cars/vehicle-detail']

    useEffect(() => {
        const queryInfo = {active: true, lastFocusedWindow: true};
        chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
            if (tabs[0] == null)
            {
                console.log(tabs)
                console.log('url error');
                return;
            }
            const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(urlCall); //set url and reset state
            // if (urlCall.includes('cars.com/vehicledetail')){
            //     setValidWebsite(website)
            // }
            var siteID = -1
            for(let i=0; i<conditions.length; i++) {
                if(urlCall.includes(conditions[i])) {
                  setValidWebsite(conditions[i])
                  siteID = i + 1
                }
            }
            
            if(siteID == 3 || siteID == 5){
                const parsedURL2 = urlCall.replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
                console.log(urlCall)
                console.log(parsedURL2)
                const fetchURL =  'http://18.207.236.241:8080/getUrl/' + parsedURL2;
                console.log(fetchURL)
            }
            else if(siteID == 1){
                const data = singleCarData1(url)
                const fetchURL =  'http://18.207.236.241:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/' + data.zip;
            }else if(siteID == 2){
                const data = singleCarData2(url)
                const fetchURL =  'http://18.207.236.241:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/' + data.zip;

            }else if(siteID == 4){
                const data = singleCarData4(url)
                const fetchURL =  'http://18.207.236.241:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/' + data.zip;
            }else{
                return;
            }

            // console.log("new version");
            
            // const parsedURL2 = urlCall.replace(/https:\/\/www\.autotrader\.com\/cars-for-sale\/vehicledetails.xhtml/g, 'constautotraderurl').replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
            // const parsedURL3 = parsedURL2.split('&')
            // console.log(urlCall)
            // console.log(parsedURL2)
            // const fetchURL =  'http://18.207.236.241:8080/getUrl/' + parsedURL3[0];
            // console.log(fetchURL)
            // const fetchURL =  'http://18.207.236.241:8080/scrape/' + response.make + '/' + response.model + '/' + response.year + '/20001'

            axios.get(fetchURL)
                .then((response) => {
                    console.log("Response: " + response)
                    setCarData(response.data);
                    setDone (true);
                    setError(null);                
                })
                .catch((error) => {
                    // Error
                    if (response.error) {
                        // The request was made and the server responded with a status code
                        // that falls out of the range of 2xx
                        console.log("Error out of 2xx Range Found:");
                        console.log(error.toJSON());
                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);
                    } else if (error.request) {
                        // The request was made but no response was received
                        // `error.request` is an instance of XMLHttpRequest in the 
                        // browser and an instance of
                        // http.ClientRequest in node.js
                        console.log("No Repsonse Received from Request");
                        console.log(error.toJSON());
                        console.log(error.request);
                    } else {
                        // Something happened in setting up the request that triggered an Error
                        console.log("Request not sent");
                        console.log('Error', error.message);
                    }
                    console.log(error.toJSON());
                    console.log(error.config)
                });  
        });

        return () => setValidWebsite('') //before next useEffect is created, set validWebsite to ''    

    }, [chrome.tabs]);

    // if (error) {
    //     return alert(error)
    // }
    // if (!carData) return null;
    if (!done){
        return(
            <div className="App">
                <ReactLoading
                    type={"balls"}
                    color={"#000000"}
                    height={70}
                    width={70}
                />
                <h2 color={"#000000"}>LOADING</h2>
            </div>
        );
    }
    else{
        if(validWebsite != ''){
            return(    
                <div className="App">
                    <header className="App-header">
                        <div class="banner">
                            <h1><b>CARCOW</b></h1>
                        </div>
                        {/* <h2>Click on the Car Info to the Listing</h2><br/> */}
                        <table>
                            {carData.map(car=>(                   
                                <tr>
                                    <td>
                                        <img src={car.imageurl} alt="Image Not Found"/>
                                        <div class="info-display">
                                            <a href = {car.url} target="_blank">
                                                <div class="car-basics">&nbsp;&nbsp;{car.year} {car.make} {car.model} {car.trim}</div>
                                                <div class="car-stats">
                                                    &nbsp; <div class="car-price">&nbsp;${car.price} </div>&nbsp; &nbsp;<div class="car-mileage"> {car.mileage}mi</div>
                                                </div>
                                                <div class="car-stats">{Math.round(100*(1 - (car.price / car.suggested))) > 0 ? <div class="suggested-price-good">&nbsp;Below Market by {Math.round(100*(1 - (car.price / car.suggested)))}%</div> : <div class="suggested-price-bad"> &nbsp;Above Market by {Math.round(-100*(1 - (car.price / car.suggested)))}%</div>}</div>
                                                
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                            ))}      
                        </table>
                    </header>
                </div>
            );
        }
        else{
            return (
                //Inside of whole return block must be enclosed in tags to compile, <div></div> or <></> work here
                <>
                    console.log('invalid site')
                    <div className="App">
                        <header className="App-header">
                            <div class="banner">
                                <h1><b>CARCOW</b></h1>
                            </div>
                            <h2>Oops! Please visit a valid site.</h2>
                                <p><a href="https://cars.com" target="_blank">Cars.com</a></p>
                                <p><a href="https://autotrader.com" target="_blank">Auto-Trader</a></p>
                                <p><a href="https://cargurus.com" target="_blank"> Car Gurus</a></p>
                                <p><a href="https://carsdirect.com" target="_blank"> Cars Direct</a></p>
                                <p><a href="https://edmunds.com" target="_blank"> Edmunds</a></p>
                        </header>
                    </div> 
                </>              
            );
        }  
    }   
};

export default App
