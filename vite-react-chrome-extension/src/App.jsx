import React, { Component, useEffect, useState, useRef, useLayoutEffect } from 'react';
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
import { createTheme, ThemeProvider } from '@mui/material/styles';

//Labels for the ends of the sliders
const pricelabels = [
    {
        value: 0,
        label: '0',
    },
    {
        value: 10,
        label: '10',
    },
];

const mileagelabels = [
    {
        value: 0,
        label: '0',
    },
    {
        value: 10,
        label: '10',
    },
];

var currentMake = ''
var currentModel = ''
var currentYear = ''
var currentTrim = ''
var currentVin = ''
var currentImg = ''
var currentPrice = ''
var currentMileage = ''
var currentUrl = ''

function checkData(data) {
    if (data !== undefined) {
      // Data is defined, continue with your code here
      console.log("Data is defined:", data);
    } else {
      // Data is still undefined, wait and check again
      console.log("Data is still undefined, waiting...");
      setTimeout(checkData, 1000); // wait for 1 second (1000 milliseconds)
    }
  }


//Theme Identifier for Sliders
const muiTheme = createTheme({
    components: {
      MuiSlider: {
        styleOverrides: {
          thumb: {
            backgroundColor: '#0ea85b', // Same green as everything else
          },
          track: {
            backgroundColor: '#0ea85b', // Lavender to offset, but complement all the green
          },
          rail: {
            backgroundColor: '#254126', // Bright Purple to offset, but complement all the green color
          },
        },
      },
    },
  });


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
        
        currentMake = make
        currentModel = model
        currentYear = year
        currentTrim = trim
        currentVin = VIN
        currentPrice = price
        currentImg = imgURL
        currentMileage = mileage
        currentUrl = url
        
        console.log('single car data response:', make)
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

//autotrader
async function singleCarData2(url) {
    console.log('AA', url)
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
    let [urlCall, setUrl] = useState('');
    const [isCars, setIsCars] = useState(false);

    const [error, setError] = useState(undefined); //Changed from useState(null)
    let [carData, setCarData] = useState(null);
    let [currentCar, setCurrent] = useState(null)
    const [done, setDone] = useState(undefined);
    const [long, setLong] = useState(undefined);
    //Determine time to wait for server response before sending error message
    const [time, setTime] = useState(undefined);
    const [resetUseEffects, setResetUseEffects] = useState(false);

    //Variable to determine if preferences form popup should be open or not
    const[preferences, setPreferences] = useState (false);

    //Variables to determine if preferences form submit button should be disabled or not based on yearValue1 and yearValue2
    const[submitDisabled, setsubmitDisabled] = useState (false);
    const[submitDisabled2, setsubmitDisabled2] = useState (false);

    //Variables to manage each Slider Component and their values
    const [pricePriority, setpricePriority] = useState(10)
    const [mileagePriority, setmileagePriority] = useState(0)

    let [yearValue1, setyearValue1] = useState(2023)
    let [yearValue2, setyearValue2] = useState(2023)

    const [trimPriority, settrimPriority] = useState(0)

    //Variable to help manage loading similar car listings for display
    const [showSimilarCars, setshowSimilarCars] = useState(false);

    //Variable to keep track of status of cars shown
    const [loadingSimilarCars, setloadingSimilarCars] = useState(false);

    //Variable to help manage loading more car listings for display
    const [moreCarsLoading, setmoreCarsLoading] = useState(false)

    let tempCarData = undefined
    const [email, setEmail] = useState('')

    //Counter variable to track how many car results we receive
    const [counter, setCounter] = useState(0)

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
        setDone(false)
        setLong(false)
        console.log("From the SliderChange function:")
        var fetchPreferences = 'http://localhost:8080/getCarData/' + currentMake + '/' + currentModel + '/' + currentYear + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
        
        if (showSimilarCars) {
            console.log("We've swithed to similar cars")
            fetchPreferences = 'http://localhost:8080/findEquivalent/' + currentModel + '/' + currentYear + '/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
        }
        
        axios.get(fetchPreferences)
        .then((response) => {
            console.log("slider change: ",response)
            setCarData(response.data);
            setDone (true);
            setLong(true)
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

    useEffect(()=>{
        console.log("change in :",carData)
    }, [carData])
    

    useEffect(async () => {
        const queryInfo = {active: true, lastFocusedWindow: true};
        // get user id and email
        // chrome.identity.getProfileUserInfo({'accountStatus': 'ANY'}, function(info) {
        //     setEmail(info.email);
        //     console.log(info);
        //     document.querySelector('textarea').value=JSON.stringify(info);
        // });


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
                var fetchURL =  'http://localhost:8080/getUrl/' + parsedURL2 + '/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 +'/NA/' + trimPriority;
                // console.log(fetchURL)
            }
            else if(siteID == 1){
                const data =  await singleCarData1(urlCall)
                var minYear = parseInt(data.year) - 2;
                var maxYear = parseInt(data.year) + 2;

                await setyearValue1(minYear)
                await setyearValue2(maxYear)
                setLong(false)
                setDone(false)

                //ALERT: make changes to singleCarData2 and 3 in the future  

                // console.log("returning: data ", currentMake)
                // console.log(currentModel)
                // console.log(currentYear)
                // console.log(data.trim)
                var fetchURL =  'http://localhost:8080/getCarData/' +  data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + 0  + '/' + 0 + '/NA/' + trimPriority;
            }else if(siteID == 2){
                const data = await singleCarData2(urlCall)
                var fetchURL =  'http://localhost:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
            }else if(siteID == 4){
                const data = await singleCarData4(urlCall)
                var fetchURL =  'http://localhost:8080/getCarData/' + data.make + '/' + data.model + '/' + data.year + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
            }
            //check if url matches last call
            await chrome.storage.sync.get(["urlCall"]).then(async (result) => {
                console.log("Last call: " + result.urlCall);
                if(urlCall == result.urlCall){
                    console.log('Url matches same page')
                    await chrome.storage.sync.get(["carData"]).then(async (result2) => {
                        // console.log("Last carData", JSON.parse(result2.carData));
                        // tempCarData = await JSON.parse(result2.carData)
                        console.log(result2)
                        if(result2.carData[0] == undefined){
                            console.log("Our URL Key exists, but value is undefined, or not matching url")
                            axios.get(await fetchURL)
                            .then((response) => {
                                // console.log("Response: ",response)
                                setCarData(response.data);
                                // console.log("cardata show on console",response.data)
                                //store response in chrome storage
                                chrome.storage.sync.set({ urlCall : urlCall }).then(() => {
                                    console.log("Url set to " + urlCall);
                                });   
                                chrome.storage.sync.set({ carData : response.data }).then(() => {
                                    console.log("carData set second: ", response.data);
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
                        else{
                            var testModel = await result2.carData[0].model
                            if(testModel != currentModel)
                            {
                                console.log('non matching model', currentModel)
                                console.log(result2.carData)
                            }
                            else{
                                setCarData(await result2.carData)
                                // console.log("awaiting: ", await carData)
                                //edge case: url exists but carData undefined
                            }  
                            if(carData == undefined){
                                console.log("Our URL Key exists, but value is undefined, or not matching url")
                                axios.get(await fetchURL)
                                .then((response) => {
                                    // console.log("Response: ",response)
                                    setCarData(response.data);
                                    // console.log("cardata show on console",response.data)
                                    //store response in chrome storage
                                    chrome.storage.sync.set({ urlCall : urlCall }).then(() => {
                                        console.log("Url set to " + urlCall);
                                    });   
                                    chrome.storage.sync.set({ carData : response.data }).then(() => {
                                        console.log("carData set second: ", response.data);
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
                        }
                        
                        
                        setDone (true);
                        setError(null); 
                    });

                    
                    
                }
                else{
                    console.log('Url does not match')
                    axios.get(await fetchURL)
                    .then((response) => {
                        // console.log("Response: ",response)
                        setCarData(response.data);
                        // console.log("cardata show on console",response.data)
                         //store response in chrome storage
                        chrome.storage.sync.set({ carData : response.data }).then(() => {
                            console.log("carData set second: ", response.data);
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

        // //Set the cache key that we will search for
        // var cacheKey = urlCall;
        // //getBackgroundPage line is necessary when trying to access the chrome.storage API from a content script or popup window
        // chrome.runtime.getBackgroundPage((backgroundPage) => {
        //     backgroundPage.chrome.storage.local.get([cacheKey], function(result){
        //         //If the cache key is found in the cache, use its data to set carData
        //         if (result.hasOwnProperty(cacheKey)) {
        //             console.log(`Found "${cacheKey}" in cache:`, result[cacheKey]);
        //             setCarData(result[cacheKey]);
        //             } 
        //         //Otherwise, key was not found in cache so make Axios call to server for response, 
        //         //then create new cache entry using the key not found in the cache
        //         else {         
        //             // console.log(fetchURL)
        //             console.log(`"${cacheKey}" not found in cache, fetching from server...`);
                     
                // }
        //     });
        // });

        setCarData(await tempCarData)
        // console.log(await carData)

        return () => {setIsCars(false)} //before next useEffect is created, set isCars to false    

    }, [chrome.tabs]);

    const preferenceFormOpen = () => {
        setPreferences(true);
    };

    //Close Preferences Form
    const preferenceFormClose = () => {
        setPreferences(false);
    };

    // replace image function
    const replaceImage = (error) => {
        //replacement of broken Image
        // error.target.src = 'C:\Users\dmurray_7\Desktop\Capstone Senior Design l\Carcow Project\Carcow\vite-react-chrome-extension\src\no_photo_available.jpg';
        error.target.src = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRT4gKDtP_saQcsAuBukz2OlfjtOh9DDMI9Edtb1iAfA_2-GI39chp5exgrelld5ViOdZw&usqp=CAU';
    }

    //Append more car entries to the list displayed in the extension
    const handleLoadMore = async() => {
        setmoreCarsLoading(true);
        console.log("Loading more cars momentarily...BE PATIENT >:(")
        console.log("current car is ",currentCar)
        var fetchMoreCars = 'http://localhost:8080/getCarData/' + currentMake + '/' + currentModel + '/' + currentYear + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;

        if (showSimilarCars) {
            fetchMoreCars= 'http://localhost:8080/findEquivalent/' + currentModel + '/' + currentYear + '/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
        }

        axios.get(fetchMoreCars)
        .then((response) => {
            console.log("We got more cars DI MOLTO!!!! ", response)
            setCarData(response.data);
            setDone (true);
            setError(null); 
            setmoreCarsLoading(false);
        })
        .catch((error) => {
            console.error(error);
            setmoreCarsLoading(false);
        });
    };

    const loadSimilar = async() => {
        setloadingSimilarCars (true);
        console.log("Loading similar cars momentarily...BE PATIENT B)")
        console.log("current car is ", currentCar)
        const fetchSimilarCars = 'http://localhost:8080/findEquivalent/' + currentModel + '/' + currentYear + '/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
        axios.get(fetchSimilarCars)
        .then((response) => {
            console.log("We got more cars!!!! ", response)
            setCarData(response.data);
            setDone (true);
            setError(null); 
            setshowSimilarCars(true);
            setloadingSimilarCars(false);
        })
        .catch((error) => {
            console.error(error);
            setshowSimilarCars(false);
            setloadingSimilarCars(false);
        });
    };

    const handleGoBack = async() => {        
        setshowSimilarCars(false);
        
        var fetchPreferences = 'http://localhost:8080/getCarData/' + currentMake + '/' + currentModel + '/' + currentYear + '/22201/' + pricePriority + '/' + mileagePriority + '/' + yearValue1 + '/' + yearValue2 + '/NA/' + trimPriority;
        
        axios.get(fetchPreferences)
        .then((response) => {
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
    }

    const formatMileageWithCommas = (mileage) => {
        return mileage.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
    };
    
    // const handleYear1 = (event) => {
    //     const inputVal = event.target.value;
    //     const parsedVal = parseInt(inputVal);
    
    //     if (/^[0-9]+$/.test(inputVal) && parsedVal >= 1900 && parsedVal <= yearValue2) {
    //         console.log("Previous Year 1: ", yearValue1);
    //         setyearValue1(parsedVal);
    //         setsubmitDisabled(false);
    //         console.log("New Year 1: ", yearValue1);
    //     }
    // };

    const handleYear1 = (event) => {
        setsubmitDisabled(true);
        const inputVal = event.target.value;
        const parsedVal = parseInt(inputVal);
        const isValidYear = /^[0-9]+$/.test(inputVal) && parsedVal >= 1900;
        const isLessThanYear2 = parsedVal <= yearValue2;
        const isTextBoxValid = isValidYear && isLessThanYear2;
        
        if (isLessThanYear2) {
            setsubmitDisabled2(false);
        }

        if (isTextBoxValid) {
          console.log("Previous Year 1: ", yearValue1);
          setyearValue1(parsedVal);
          setsubmitDisabled(false);
          console.log("New Year 1: ", yearValue1);
        }
        else {
            console.log("Input Invalid, Failed to Set Year 1")

            setyearValue1(parsedVal);
            setsubmitDisabled(true);
        }
    };

    // const handleYear2 = (event) => {
    //     const inputVal = event.target.value;
    //     const parsedVal = parseInt(inputVal);

    //     if (/^[0-9]+$/.test(inputVal) && parsedVal >= yearValue2 && parsedVal <= 2023) {
    //         console.log("Previous Year 2: ", yearValue2)
    //         setyearValue2(parsedVal); 
    //         setsubmitDisabled2(false);
    //         console.log("New Year 2: ", yearValue2)     
    //     }
    // };
    const handleYear2 = (event) => {
        setsubmitDisabled2(true);
        const inputVal = event.target.value;
        const parsedVal = parseInt(inputVal);
        const isValidYear = /^[0-9]+$/.test(inputVal) && parsedVal <= 2023;
        const isGreaterThanYear1 = parsedVal >= yearValue1;
        const isTextBoxValid = isValidYear && isGreaterThanYear1;

        if (isGreaterThanYear1) {
            setsubmitDisabled(false);
        }
      
        if (isTextBoxValid) {
          console.log("Previous Year 2: ", yearValue2);
          setyearValue2(parsedVal);
          setsubmitDisabled2(false);
          console.log("New Year 2: ", yearValue2);
        }
        else {
            console.log("Input Invalid, Failed to Set Year 2")
            setyearValue2(parsedVal);
            setsubmitDisabled2(true);
        }
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
    
    else{
        if(carData == null){
            return(
                <div className="App">
                    <header className="App-header">
                        <div class="banner">
                            <h1><b>WHEEL DEAL</b></h1>
                        </div>
                        {/* <h3>{!email == ''? email:'Please log in'}</h3> */}
                        <h3>No Response from server</h3>
                    </header>
                </div>
            )
        }
        if(isCars){
            return(  
                <div className="App">
                    <header className="App-header">
                        <view>{console.log(carData)}</view>
                        <div class="banner">
                            <h1><b>WHEEL DEAL</b></h1>
                        {/* </div>
                        <h3>{!email == ''? email:'Please log in'}</h3>
                        <div className="preferences-form"> */}
                            {!preferences?
                                <Tooltip title="Open Preferences Menu">
                                    <IconButton 
                                        className="preference-toggle" 
                                        variant='contained'
                                        sx={{color:"white", position:"absolute", top: -2, right: 0}} 
                                        onClick={preferenceFormOpen}
                                    >
                                        <BuildIcon/>
                                    </IconButton>
                                </Tooltip>:
                                <Tooltip title="Close Preferences Menu">
                                    <IconButton 
                                        className="preference-toggle" 
                                        variant='contained'
                                        sx={{color:"white", position:"absolute", top: -2, right: 0}} 
                                        onClick={preferenceFormClose}
                                    >
                                        <CloseOutlinedIcon/>
                                    </IconButton>
                                </Tooltip> 
                            }                     
                        </div>
                        {(!showSimilarCars && !loadingSimilarCars) && (
                            <button class="load-similar-button" onClick={loadSimilar}>Load Similar Cars</button>
                        )} 
                        {(!showSimilarCars && loadingSimilarCars) && <div className="loading-more">Loading...</div>}
                        {(showSimilarCars && !loadingSimilarCars) && (<button className="leave-similar-button" onClick={handleGoBack}>Back</button>)}
                        <table>
                            {carData.map((car) =>(                   
                                <>             
                                {car.VIN == currentVin ?
                                  <tr className="vin-match">
                                    {console.log(currentVin)}
                                      <td className="image-display"><img src={currentImg} alt="Image Not Found" onError={replaceImage}/></td>
                                      <td class="info-display-current">
                                          <a href = {car.url} target="_blank">
                                              {/* <div class="car-basics-current">{car.year} {car.make} {car.model} {car.trim}</div> */}
                                              {/* <div class="car-stats">
                                                  <div class="car-price">${car.price} </div>&nbsp;&nbsp;<div class="car-mileage"> {car.mileage}mi</div>
                                              </div> */}
                                              <div> <b>{"\n"}</b></div>
                                              {(car.price - car.suggested) < 0 ? <div class="suggested-price-current">Below Market by ${(parseInt(car.suggested - car.price))}</div> : <div class="suggested-price-bad"> Above Market by ${(parseInt(car.price - car.suggested))}</div>}
                                          </a>
                                      </td>
                                  </tr> :
                                  <tr className="other-cars">
                                    <td className="image-display"><img src={car.imageurl} alt="Image Not Found" onError={replaceImage}/></td>
                                    <td class="info-display">
                                        <a href = {car.url} target="_blank">
                                            <div class="car-basics">{car.year} {car.make} {car.model} {car.trim}</div>
                                            <div class="car-stats">
                                                <div class="car-price">${car.price.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')}</div>&nbsp;&nbsp;{parseInt(car.mileage) >= 1000 ? <div class="car-mileage">{formatMileageWithCommas(car.mileage)} mi</div> : <div class="car-mileage">{car.mileage} mi</div>}
                                            </div>
                                            {(car.price - car.suggested) < 0 ? <div class="suggested-price-good">Below Market by ${(parseInt(car.suggested - car.price))}</div> : <div class="suggested-price-bad"> Above Market by ${(parseInt(car.price - car.suggested))}</div>}
                                        </a>
                                    </td>
                                  </tr>
                              }
                            </>
                            ))} 
                        </table>
                        {moreCarsLoading && <div className="loading-more">Loading...</div>}
                        {!moreCarsLoading && (
                            <button class="load-more-button" onClick={handleLoadMore}>Load More Cars</button>
                        )} 
                    </header>
                    <div> 
                        {/*If preferences = true, open popup, otherwise it is false and should be closed */}
                        {preferences?
                        <div className="popup">
                            <div className="preferences-form-header"><h2>Preferences</h2></div>
                            {/* <div className="price-slider-display">
                                <h3>Price </h3><input type='range' className={pricePriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={pricePriority} onChange={(e) => setpricePriority(e.target.value)}/>
                                <h1>{pricePriority}</h1>
                            </div> */}
                            <ThemeProvider theme={muiTheme}>
                                <Box 
                                    sx={{
                                        width:280,
                                    }}
                                    spacing={3}
                                    alignItems='center'
                                    justifyContent='center'
                                    padding='5px !important'
                                    margin="5px !important"
                                >
                                    <Stack spacing={4} direction="row" sx={{mb: 1}} justifyContent="center" alignItems="center">
                                        <p class="slider-name">Price&nbsp;&nbsp;</p>
                                        <Slider 
                                            aria-label="priceSlider" 
                                            value={pricePriority} 
                                            min={0}
                                            max={10}
                                            step={1}
                                            marks={pricelabels}
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
                                            marks={mileagelabels}
                                            valueLabelDisplay="auto"
                                            onChange={(e) => setmileagePriority(e.target.value)}
                                        />
                                    </Stack>
                                    {/* <div className="year-slider-display">
                                        <h3>Year </h3><input type='range' className={yearValue1<5 ? 'low': 'high'} min='0' max='10' step='1' value={yearValue1} onChange={(e) => setyearValue1(e.target.value)}/>
                                        <h1>{yearValue1}</h1>
                                    </div> */}
                                    <div className="year-range-instructions"><h4>&nbsp;Please Enter a Year Range in the Boxes Below:</h4></div>
                                    <Stack  
                                        sx={{ mb: -1 }}
                                        direction='row'
                                        spacing={2}
                                        justifyContent='center'
                                        alignItems='center'
                                    >
                                        <input
                                            id="input1"
                                            type="text"
                                            style={{width:'85px'}}
                                            defaultValue={yearValue1}
                                            placeholder="Enter Min Year"
                                            onChange={handleYear1}
                                            min="1900"
                                            max={yearValue2}
                                            pattern="[0-9]*"
                                            minLength={4}
                                            maxLength={4}
                                        />
                                        <input
                                            id="input2"
                                            type="text"
                                            style={{width:'85px'}}
                                            defaultValue={yearValue2}
                                            placeholder="Enter Max Year"
                                            onChange={handleYear2}
                                            min={yearValue1}
                                            max="2023"
                                            pattern="[0-9]*"
                                            minLength={4}
                                            maxLength={4}
                                        />
                                        <br />
                                        {(yearValue1.length === 4 && (yearValue1 < 1900 || yearValue1 > yearValue2)) ? (
                                            <p style={{ color:'red', alignItems:'center' }}>Minimum Year must be between 1900 and Maximum Year</p>
                                        ) : ""}

                                        {(yearValue2.length === 4 && (yearValue2 < yearValue1 || yearValue2 > 2023)) ? (
                                            <p style={{ color:'red', alignItems:'center' }}>Maximum Year must be between Minimum Year and 2023</p>
                                        ) : ""}
                                    </Stack>
                                </Box>
                            </ThemeProvider>
                            {/* <div>
                                <h3>Trim </h3><input type='range' className={trimPriority<5 ? 'low': 'high'} min='0' max='10' step='1' value={trimPriority} onChange={(e) => settrimPriority(e.target.value)}/>
                                <div className="priority-value">
                                    <p1>{trimPriority}</p1>
                                </div>
                            </div> */}
                            <br />
                            {(submitDisabled || submitDisabled2) ? (<button class="disabled-button" onClick={SliderChange} disabled>Apply Preferences</button>) : (<button class="submit" onClick={SliderChange}>Apply Preferences</button>) }                 
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
