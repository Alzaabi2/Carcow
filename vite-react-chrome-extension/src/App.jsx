import React, { Component, useEffect, useState } from 'react';
import './App.css';
import './slider.css';
import $ from "jquery";
import axios from 'axios';
import ReactLoading from "react-loading";
import ReactSlider from "react-slider";
import SlidingPane from "react-sliding-pane";
import "react-sliding-pane/dist/react-sliding-pane.css";
import { findAllByTestId } from '@testing-library/react';
// import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
//import 'react-loading-skeleton/dist/skeleton.css';

// function UserPreferencesSlider() {

//     const [node, setNode] = useState(0)
//     const [node2, setNode2] = useState(0)
//     const [node3, setNode3] = useState(0)
//     const [node4, setNode4] = useState(0)
//     const [node5, setNode5] = useState(0)
//     const [node6, setNode6] = useState(0)
   
//     return(
//         <>
//             <div>
//                 <h3>Color </h3><input type='range' className={node<5 ? 'low': 'high'} min='0' max='10' step='1' value={node} onChange={(e)=>setNode(e.target.value)}/>
//                 <h1>{node}</h1>
//             </div>
//             <div>
//                 <h3>Price </h3><input type='range' className={node2<5 ? 'low': 'high'} min='0' max='10' step='1' value={node2} onChange={(e)=>setNode2(e.target.value)}/>
//                 <h1>{node2}</h1>
//             </div>
//             <div>
//                 <h3>Mileage </h3><input type='range' className={node3<5 ? 'low': 'high'} min='0' max='10' step='1' value={node3} onChange={(e)=>setNode3(e.target.value)}/>
//                 <h1>{node3}</h1>
//             </div>
//             <div>
//                 <h3>Distance </h3><input type='range' className={node4<5 ? 'low': 'high'} min='0' max='10' step='1' value={node4} onChange={(e)=>setNode4(e.target.value)}/>
//                 <h1>{node}</h1>
//             </div>
//             <div>
//                 <h3>Year </h3><input type='range' className={node5<5 ? 'low': 'high'} min='0' max='10' step='1' value={node5} onChange={(e)=>setNode5(e.target.value)}/>
//                 <h1>{node5}</h1>
//             </div>
//             <div>
//                 <h3>Trim </h3><input type='range' className={node6<5 ? 'low': 'high'} min='0' max='10' step='1' value={node6} onChange={(e)=>setNode6(e.target.value)}/>
//                 <h1>{node6}</h1>
//             </div>
//         </>
//     );
// };

{/* <SlidingPane
                        isOpen={pane.isPaneOpen}
                        title="Preferences Panel"
                        from="right"
                        width="200px"
                    ></SlidingPane> */}
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
    //Determine time to wait for server response before sending error message
    const [time, setTime] = useState(undefined);

    //Variable to determine if preferences form popup should be open or not
    const[preferences, setPreferences] = useState (false);

    //Variables to manage each Slider Component and their values
    const [pricePriority, setpricePriority] = useState(0)
    const [mileagePriority, setmileagePriority] = useState(0)
    const [yearPriority, setyearPriority] = useState(0)
    const [trimPriority, settrimPriority] = useState(0)


    const SliderChange = () => {
        console.log("Old Price Priority: " + pricePriority);
        console.log("Old Mileage Priority: " + mileagePriority);
        console.log("Old Year Priority: " + yearPriority);
        console.log("Old Trim Priority: " + trimPriority);
        (event) => setpricePriority(event.target.value);
        (event2) => setmileagePriority(event2.target.value);
        (event3) => setyearPriority(event3.target.value);
        (event4) => settrimPriority (event4.target.value);
        console.log("New Price Priority: " + pricePriority);
        console.log("New Mileage Priority: " + mileagePriority);
        console.log("New Year Priority: " + yearPriority);
        console.log("New Trim Priority: " + trimPriority);
    };

        // + '/preferences/' + pricePriority + '/' + mileagePriority + '/' + yearPriority + '/' + trimPriority + '/'

    /*
     * Get current URL
     */
    const conditions = ['cars.com/vehicledetail', 'cargurus.com', 'autotrader.com/cars-for-sale/vehicledetails', 'carsdirect.com/used_cars/vehicle-detail', 'edmunds.com']
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
                    //If the URL contains any string in the conditions array, setIsCars to true
                    setIsCars(true)
                }
            }
            
            console.log("new version");
            const parsedURL2 = urlCall.replace(/https:\/\/www\.autotrader\.com\/cars-for-sale\/vehicledetails.xhtml/g, 'constautotraderurl').replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
            console.log(urlCall)
            console.log(parsedURL2)
            //According to Stack Overflow, API URL shouldn't be hardcoded
            //Have to use the URL depending on teh environment the code is being run on
            // localhost on development and the production API URL on production)
            //**Curent issue: Not connecting to the server properly with this hardcoded URL */
            //Previous server IP: 18.207.236.241:8080
            //Changed server IP to: 172.26.142.227:8080
            //Now changed to: localhost:8080
            const fetchURL =  'http://localhost:8080/getUrl/' + parsedURL2;
            console.log(fetchURL)
                  setValidWebsite(conditions[i])
                  siteID = i + 1
                }
            }
            
            if(siteID == 3 || siteID == 5){
                const parsedURL2 = urlCall.replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
                console.log(urlCall)
                console.log(parsedURL2)
                const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL2;
                console.log(fetchURL)
            }
            else if(siteID == 1){
                const data = singleCarData1(url)
                const fetchURL =  'http://127.0.0.1:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/' + data.zip;
            }else if(siteID == 2){
                const data = singleCarData2(url)
                const fetchURL =  'http://127.0.0.1:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/' + data.zip;

            }else if(siteID == 4){
                const data = singleCarData4(url)
                const fetchURL =  'http://127.0.0.1:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/' + data.zip;
            }else{
                return;
            }

            // console.log("new version");
            
            // const parsedURL2 = urlCall.replace(/https:\/\/www\.autotrader\.com\/cars-for-sale\/vehicledetails.xhtml/g, 'constautotraderurl').replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
            // const parsedURL3 = parsedURL2.split('&')
            // console.log(urlCall)
            // console.log(parsedURL2)
            // const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL3[0];
            // console.log(fetchURL)
            // const fetchURL =  'http://127.0.0.1:8080/scrape/' + response.make + '/' + response.model + '/' + response.year + '/20001'

            axios.get(fetchURL)
                .then((response) => {
                    console.log("Response: " + response)
                    setCarData(response.data);
                    setDone (true);
                    setError(null);                
                }, {timeout: 15000})
                .catch((error) => {
                    // Error
                    setTime(true);
                    if (error.response) {
                        // The request was made and the server responded with a status code
                        // that falls out of the range of 2xx
                        console.log("Error out of 2xx Range Found:");
                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);

                    } else if (error.request) {
                        // The request was made but no response was received
                        // `error.request` is an instance of XMLHttpRequest in the 
                        // browser and an instance of http.ClientRequest in node.js
                        console.log("No Repsonse Received from Request");
                        console.log(error.request);
                    } else {
                        // Something happened in setting up the request that triggered an Error
                        console.log("Request not sent");
                        console.log('Error', error.message);
                    }
                    console.log(error.config);
                });  
        });

        return () => setValidWebsite('') //before next useEffect is created, set validWebsite to ''    

    }, [chrome.tabs]);

    useEffect(() => {
        const fetchPreferences =  'http://localhost:8080/getPreferences/' + pricePriority + '/' + mileagePriority + '/' + yearPriority + '/' + trimPriority + '/';
            console.log(fetchPreferences)
            axios.get(fetchPreferences)
                .then((response) => {
                    console.log("Response: " + response)
                    setCarData(response.data);
                    setDone (true);         
                }, {timeout: 15000})
                .catch((error) => {
                    // Error
                    setTime(true);
                    if (error.response) {
                        // The request was made and the server responded with a status code
                        // that falls out of the range of 2xx
                        console.log("Error out of 2xx Range Found:");
                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);

                    } else if (error.request) {
                        // The request was made but no response was received
                        // `error.request` is an instance of XMLHttpRequest in the 
                        // browser and an instance of http.ClientRequest in node.js
                        console.log("No Repsonse Received from Request");
                        console.log(error.request);
                    } else {
                        // Something happened in setting up the request that triggered an Error
                        console.log("Request not sent");
                        console.log('Error', error.message);
                    }
                    console.log(error.config);
                });  
    }, []);

    //pricePriority, mileagePriority, yearPriority, trimPriority
    // if (error) {
    //     return alert(error)
    // }
    // if (!carData) return null;

    //Open Preferences Form
    const preferenceFormOpen = () => {
        setPreferences(!preferences);
    };

    //Close Preferences Form
    const preferenceFormClose = () => {
        setPreferences(!preferences);
    };

    if (!done && !time){
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
    // else if (!done && time){
    //     return (
    //         <div className="App">
    //             <div class="banner">
    //                 <h1><b>CARCOW</b></h1>
    //             </div>
    //             <h3>{error.response.status} Status Error Code</h3>
    //             <p>{error.response.data}</p>
    //         </div>              
    //     ); 
    // }
    else{
        if(isCars){
            return(  
            }
        if(validWebsite != ''){
            return(    
                <div className="App">
                    <header className="App-header">
                        <view>{console.log(carData)}</view>
                        <div class="banner">
                            <h1><b>WHEEL DEAL</b></h1>
                        </div>
                        <div className="preferences-form">
                            {!preferences?
                            <button onClick={preferenceFormOpen}>
                               Open Preferences
                            </button>: <button onClick={preferenceFormClose}>
                               Close Preferences
                            </button>}
                        </div>
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
                    <div> 
                        {/*If preferences = true, open popup, otherwise it is false and should be closed */}
                        {preferences?
                        <div className="popup">
                            <div>
                                <h3>Price </h3><input type='range' className={pricePriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={pricePriority} onChange={(e) => setpricePriority(e.target.value)}/>
                                <h1>{pricePriority}</h1>
                            </div>
                            <div>
                                <h3>Mileage </h3><input type='range' className={mileagePriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={mileagePriority} onChange={(e) => setmileagePriority(e.target.value)}/>
                                <h1>{mileagePriority}</h1>
                            </div>
                            <div>
                                <h3>Year </h3><input type='range' className={yearPriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={yearPriority} onChange={(e) => setyearPriority(e.target.value)}/>
                                <h1>{yearPriority}</h1>
                            </div>
                            <div>
                                <h3>Trim </h3><input type='range' className={trimPriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={trimPriority} onChange={(e) => settrimPriority(e.target.value)}/>
                                <h1>{trimPriority}</h1>
                            </div>
                            <div className="submit">
                                <button onClick={SliderChange}>Apply Preferences</button>
                            </div>
                        </div>: ""}
                    </div>
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
                                <h1><b>WHEEL DEAL</b></h1>
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

