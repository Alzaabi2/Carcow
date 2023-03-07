import React, { Component, useEffect, useState, useRef } from 'react';
import './App.css';
import './slider.css';
import $, { data } from "jquery";
import axios from 'axios';
import ReactLoading from "react-loading";
import cheerio from 'cheerio';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Slider from '@mui/material/Slider';
import BuildIcon from '@mui/icons-material/Build';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';

//Labels for the ends of the sliders
const labels = [
    {
        value: 0,
        label: '0',
    },
    {
        value: 10,
        label: '10',
    },
];

//cars.com
async function singleCarData1(url) {
    const carData = await axios.get(url)
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
        // console.log(`Year: ${year}`);
        // console.log(`Make: ${make}`);
        // console.log(`Model: ${model}`);
        // console.log(`Trim: ${trim}`);
        return {year, make, model, trim}
        // Print the scraped data
    })
    .catch((error) => {
        console.error(error);
    });

    return carData
}

//autotrader
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

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
        return {year, make, model, trim}
    })
    .catch((error) => {
        console.error(error);
    });
}

//edmunds
async function singleCarData4(url) {
    const carData = await axios.get(url)
    .then((response) => {
        // Load the HTML into cheerio
        var $ = cheerio.load(response.data);

        // Select the element that contains the data we want to scrape
        // In this example, we want to scrape the title of the car
        var title = $('h1[class="not-opaque text-black d-inline-block mb-0 size-24"]').text();

        // Split the title into its parts (year, make, model, trim)
        var titleParts = title.split(' ');
        console.log(titleParts)
        var zip = 20001
        // Extract the year, make, model, and trim from the title
        var year = titleParts[0];
        var make = titleParts[1];
        if(titleParts[1])
        //special case for tesla:
        if (make.toLowerCase() == 'tesla'){
            if (model.toLowerCase().replace(' ', '') == 'model'){
                model = titleParts[2] + ' ' + titleParts[3]
            }
            console.log(`Year: ${year}`);
            console.log(`Make: ${make}`);
            console.log(`Model: ${model}`);
            return {year, make, model, trim}
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
            return {year, make, model, trim}
        }
        var model = titleParts[2];
        

        // Print the scraped data
        console.log(`Year: ${year}`);
        console.log(`Make: ${make}`);
        console.log(`Model: ${model}`);
        console.log(`Trim: ${trim}`);
        return {year, make, model, trim}

    })
    .catch((error) => {
        console.error(error);
    });
}

function App() {
    const [urlCall, setUrl] = useState('');
    const [isCars, setIsCars] = useState(false);

    const [error, setError] = useState(undefined); //Changed from useState(null)
    const [carData, setCarData] = useState(null);
    const [done, setDone] = useState(undefined);
    const [long, setLong] = useState(undefined);
    //Determine time to wait for server response before sending error message
    const [time, setTime] = useState(undefined);
    const [resetUseEffects, setResetUseEffects] = useState(false);

    //Variable to determine if preferences form popup should be open or not
    const[preferences, setPreferences] = useState (false);

    //Variables to manage each Slider Component and their values
    const [pricePriority, setpricePriority] = useState(0)
    const [mileagePriority, setmileagePriority] = useState(0)
    const [yearPriority, setyearPriority] = useState(0)
    const [trimPriority, settrimPriority] = useState(0)

    const [testValue, settestValue] = useState (0)

        // console.log('running chrome local')
        // const value = '2'
        // console.log("chrome storage "+ chrome.storage)
        //     chrome.storage.sync.set({ key: value }).then(() => {
        //         console.log("Value is set to " + value);
        //     });
            
        //     chrome.storage.sync.get(["key"]).then((result) => {
        //         console.log("Value currently is " + result.key);
        //     });
    /*
     * Get current URL
     */
    const conditions = ['cars.com/vehicledetail', 'autotrader.com/cars-for-sale/vehicledetails', 'cargurus.com/cars', 'edmunds.com', 'carsdirect.com/used_cars/vehicle-detail']

    const SliderChange = async() => {
        console.log("From the SliderChange function:")
        const fetchPreferences = 'http://localhost:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearPriority + '/NA/' + trimPriority;
        axios.get(fetchPreferences)
        .then((response) => {
            console.log("slider change: ",response)
            setCarData(response.data);
            setDone (true);
            setError(null); 
        })
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
        console.log("End of SliderChange Function results");
        preferenceFormClose();
    };

    // useEffect(() => {
    //     console.log("The SliderChange() useEffect was utilized");
    //     SliderChange();
    // }, [pricePriority, mileagePriority, yearPriority, trimPriority]);
    

    useEffect(async () => {
        const queryInfo = {active: true, lastFocusedWindow: true};
        

        chrome.tabs && chrome.tabs.query(queryInfo, async tabs => {
            if (tabs[0] == null)
            {
                console.log(tabs)
                console.log('url error');
                return;
            }
            const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(urlCall); //set url and reset state
            // if (urlCall.includes('cars.com/vehicledetail')){
            //     setIsCars(true) //set isCars to true
            // }

            var siteID = -1
            for(let i=0; i<conditions.length; i++) {
                if(urlCall.includes(conditions[i])) {
                  setIsCars(true)
                  siteID = i + 1
                }
            }

            if(siteID == 3 || siteID == 5){
                const parsedURL2 = urlCall.replace(/https:\/\/www\.autotrader\.com\/cars-for-sale\/vehicledetails.xhtml/g, 'constautotraderurl').replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colum').replace(/\?/g, 'questionmark')
                console.log(urlCall)
                console.log(parsedURL2)
                var fetchURL =  'http://localhost:8080/getUrl/' + parsedURL2 + '/' + pricePriority + '/' + mileagePriority + '/' + yearPriority +'/NA/' + trimPriority;
                // console.log(fetchURL)
            }
            else if(siteID == 1){
                const data =  await singleCarData1(urlCall)
                console.log("returning: "+data.make)
                console.log(data.model)
                console.log(data.year)
                console.log(data.trim)
                var fetchURL =  'http://localhost:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearPriority +'/NA/' + trimPriority;
            }else if(siteID == 2){
                const data = await singleCarData2(urlCall)
                var fetchURL =  'http://localhost:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearPriority +'/NA/' + trimPriority;
            }else if(siteID == 4){
                const data = await singleCarData4(urlCall)
                var fetchURL =  'http://localhost:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearPriority +'/NA/' + trimPriority;
            }

            //check if url matches last call
            await chrome.storage.sync.get([urlCall]).then((result) => {
                console.log("Get1: Previous key is: ", result.urlCall);
                
                if(urlCall == result.urlCall){
                    console.log('Url matches existing URL in storage')
                    chrome.storage.sync.get(["carData"]).then(async (result2) => {
                        console.log("Get2: Previous carData is: ", result2.data)
                        const tempCarData = JSON.stringify(result2.carData)
                        setCarData (result2.carData, () => {
                            console.log("carData now set to: ", carData)
                        })
                        // console.log("Waiting: ", tempCarData)
                        // console.log("Awaiting Car Data: ", carData)
                        //edge case: url key exists but its value, carData, is undefined
                        if(result2.carData == undefined){
                            console.log("Our URL Key exists, but value is undefined")
                            axios.get(fetchURL)
                            .then((response) => {
                                console.log("Response: ",response)
                                setCarData(response.data);
        
                                //store response in chrome storage
                                chrome.storage.sync.set({ carData : response.data }).then(() => {
                                    console.log("Set1: carData set from undefined to: ", response.data);
                                });
                                // const cacheEntry = {};
                                // cacheEntry[cacheKey] = response.data;
                                // //onIstalled.addListener line initializes the chrome.storage API on extension installation or update (necessary to do this)
                                // chrome.runtime.onInstalled.addListener ( () => {
                                //     chrome.storage.local.set(cacheEntry, function() {
                                //         console.log(response.data);
                                //         console.log(`Successfully stored cache key: "${cacheKey}" and its data:`, result[cacheKey]);
                                //     });
                                // });
                                //End of Cache Entry Creation
                                setDone (true);
                                setError(null);                
                            }, {timeout: 15000})
                            .catch((error) => {
                                // Error
                                setLong(true);
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
                        }
                    }, {timeout: 5000});                   
                }
                else{
                    console.log('Url does not match')
                    axios.get(fetchURL)
                    .then((response) => {
                        console.log("Response: ",response)
                        setCarData(response.data);
                        console.log("cardata show on console",response.data)
                         //store response in chrome storage
                        chrome.storage.sync.set({ carData : response.data }).then(() => {
                            console.log("Set2: carData set as: ", response.data);
                        });

                        // const cacheEntry = {};
                        // cacheEntry[cacheKey] = response.data;
                        // //onIstalled.addListener line initializes the chrome.storage API on extension installation or update (necessary to do this)
                        // chrome.runtime.onInstalled.addListener ( () => {
                        //     chrome.storage.local.set(cacheEntry, function() {
                        //         console.log(response.data);
                        //         console.log(`Successfully stored cache key: "${cacheKey}" and its data:`, result[cacheKey]);
                        //     });
                        // });
                        //End of Cache Entry Creation
                        setDone (true);
                        setError(null);                
                    }, {timeout: 15000})
                    .catch((error) => {
                        // Error
                        setLong(true);
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
                }
            });
            console.log("We've exited the main chrome.storage.sync.get function");
            //store url in chrome storage
            chrome.storage.sync.set({ urlCall : urlCall }).then(() => {
                console.log("Url set to " + urlCall);
            });         
        });
        return () => {setIsCars(false)} //before next useEffect is created, set isCars to false    

    }, [chrome.tabs]);

    const preferenceFormOpen = () => {
        setPreferences(true);
    };

    //Close Preferences Form
    const preferenceFormClose = () => {
        setPreferences(false);
    };

    const handleChange = () => {
        console.log("New Test Value: "+ testValue);
    };

    if (!done && !long){
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
                <div className="App">
                    <header className="App-header">
                        <view>{console.log(carData)}</view>
                        <div class="banner">
                            <h1><b>WHEEL DEAL</b></h1>
                            {!preferences?
                                <Tooltip title="Open Preferences Menu">
                                    <IconButton 
                                        className="preference-toggle" 
                                        variant='contained'
                                        sx={{color:"white", position:"fixed", top: 20, right: 0}} 
                                        onClick={preferenceFormOpen}
                                    >
                                        <BuildIcon/>
                                    </IconButton>
                                </Tooltip>:
                                <Tooltip title="Close Preferences Menu">
                                    <IconButton 
                                        className="preference-toggle" 
                                        variant='contained'
                                        sx={{color:"white", position:"fixed", top: 20, right: 0}} 
                                        onClick={preferenceFormClose}
                                    >
                                        <CloseOutlinedIcon/>
                                    </IconButton>
                                </Tooltip> 
                            }                     
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
                            <div className="preferences-form-header"><h2>Preferences Form</h2></div>
                            {/* <div className="price-slider-display">
                                <h3>Price </h3><input type='range' className={pricePriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={pricePriority} onChange={(e) => setpricePriority(e.target.value)}/>
                                <h1>{pricePriority}</h1>
                            </div> */}
                            <Box 
                                sx={{width:250}}
                                alignItems = "center"
                            >
                                <Stack spacing={4} direction="row" sx={{mb: 1}} justifyContent="center" alignItems="center">
                                    <p class="slider-name">Price</p>
                                    <Slider 
                                        aria-label="priceSlider" 
                                        value={pricePriority} 
                                        min={0}
                                        max={10}
                                        step={1}
                                        marks={labels}
                                        valueLabelDisplay="auto"
                                        onChange={(e) => setpricePriority(e.target.value)}
                                    />
                                </Stack>
                                {/* <div className="mileage-slider-display">
                                    <h3>Mileage </h3><input type='range' className={mileagePriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={mileagePriority} onChange={(e) => setmileagePriority(e.target.value)}/>
                                    <h1>{mileagePriority}</h1>
                                </div> */}
                                <Stack spacing={3} direction="row" sx={{mb: 1}} justifyContent="center" alignItems="center">
                                    <p class="slider-name">Mileage</p>
                                    <Slider 
                                        aria-label="mileageSlider" 
                                        value={mileagePriority} 
                                        min={0}
                                        max={10}
                                        step={1}
                                        marks={labels}
                                        valueLabelDisplay="auto"
                                        onChange={(e) => setmileagePriority(e.target.value)}
                                    />
                                </Stack>
                                {/* <div className="year-slider-display">
                                    <h3>Year </h3><input type='range' className={yearPriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={yearPriority} onChange={(e) => setyearPriority(e.target.value)}/>
                                    <h1>{yearPriority}</h1>
                                </div> */}
                                <Stack spacing={4} direction="row" sx={{mb: 1}} justifyContent="center" alignItems="center">
                                    <p class="slider-name">Year</p>
                                    <Slider 
                                        aria-label="yearSlider" 
                                        value={yearPriority} 
                                        min={0}
                                        max={10}
                                        step={1}
                                        marks={labels}
                                        valueLabelDisplay="auto"
                                        onChange={(e) => setyearPriority(e.target.value)}
                                    />
                                </Stack>
                            </Box>
                            {/* <div>
                                <h3>Trim </h3><input type='range' className={trimPriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={trimPriority} onChange={(e) => settrimPriority(e.target.value)}/>
                                <div className="priority-value">
                                    <p1>{trimPriority}</p1>
                                </div>
                            </div> */}
                            <button class="submit" onClick={SliderChange}>Apply Preferences</button>&nbsp;
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
