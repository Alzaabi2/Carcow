import React, { useEffect, useState, useRef } from 'react';
import './App.css';
import $ from "jquery";
import axios from 'axios';
import ReactLoading from "react-loading";

const cheerio = require('cheerio')
const rp = require('request-promise')

async function singleCarData1(url) {
  try {
    const html = await rp(url)
    const $ = cheerio.load(html)

    // find title text from class
    const titleObj = $('h1.listing-title')
    if (!titleObj) {
      titleObj = $('h1.sticky-header-listing-title')
    }
    const title = titleObj.text()

    const titleParts = title.split(' ', 3)

    // find make
    const make = titleParts[1]

    // find model
    const model = titleParts[2]

    // find year
    const year = titleParts[0]

    // find trim(optional)
    const trim = titleParts[3]

    // Create and Return a dictionary {make: ..., model: ..., trim: ..., year: ...} for single car
    return {
      make,
      model,
      trim,
      year
    }
  } catch (err) {
    console.error(err)
  }
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
            const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(urlCall); //set url and reset state
            // if (urlCall.includes('cars.com/vehicledetail')){
            //     setValidWebsite(website)
            // }
            for(let i=0; i<conditions.length; i++) {
                if(urlCall.includes(conditions[i])) {
                  setValidWebsite(conditions[i])
                }
            }
            
            console.log("new version");
            
            const parsedURL2 = urlCall.replace(/https:\/\/www\.autotrader\.com\/cars-for-sale\/vehicledetails.xhtml/g, 'constautotraderurl').replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
            const parsedURL3 = parsedURL2.split('&')
            console.log(urlCall)
            console.log(parsedURL2)
            const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL3[0];
            console.log(fetchURL)
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
