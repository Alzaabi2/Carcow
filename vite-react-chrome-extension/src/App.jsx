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

function App() {
    const [urlCall, setUrl] = useState('');
    const [isCars, setIsCars] = useState(false);

    const [error, setError] = useState(undefined); //Changed from useState(null)
    const [carData, setCarData] = useState(null);
    const [done, setDone] = useState(undefined);
    //Determine time to wait for server response before sending error message
    const [time, setTime] = useState(undefined);

    //Variable to determine if preferences form popup should be open or not
    const[preferences, setPreferences] = useState (false);

    //Variables to manage each Slider Component
    //const [node, setNode] = useState(0)
    const [node2, setNode2] = useState(0)
    const [node3, setNode3] = useState(0)
    //const [node4, setNode4] = useState(0)
    const [node5, setNode5] = useState(0)
    const [node6, setNode6] = useState(0)

    const [prefPrice, setprefPrice] = useState(0)
    const [prefMileage, setprefMileage] = useState(0)
    const [prefYear, setprefYear] = useState(0)
    const [prefTrim, setprefTrim] = useState(0)


    /*
     * Get current URL
     */
    const conditions = ['cars.com/vehicledetail', 'cargurus.com', 'autotrader.com/cars-for-sale/vehicledetails', 'carsdirect.com/used_cars/vehicle-detail', 'edmunds.com']

    useEffect(() => {
        const queryInfo = {active: true, lastFocusedWindow: true};

        chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
            const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(urlCall); //set url and reset state
            // if (urlCall.includes('cars.com/vehicledetail')){
            //     setIsCars(true) //set isCars to true
            // }
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
            const fetchURL =  'http://localhost:8080/getUrl/' + parsedURL2 + '/preferences/' + prefPrice + '/' + prefMileage + '/' + prefYear + '/' + prefTrim + '/';
            console.log(fetchURL)
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

        return () => setIsCars(false) //before next useEffect is created, set isCars to false    

    }, [chrome.tabs]);

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

    const SliderChange = () => {
        const handlePriceSliderChange = (event) => {
          setprefPrice(event.target.value);
        };
      
        const handleMileageSliderChange = (event) => {
          setprefMileage(event.target.value);
        };
      
        const handleYearSliderChange = (event) => {
          setprefYear(event.target.value);
        };

        const handleTrimSliderChange = (event) => {
            setprefTrim (event.target.value);
        }
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
        if (isCars === 'null'){
            return (
                <>
                    console.log('No Car Data Found')
                    <div className="App">
                        <header className="App-header">
                            <div class="banner">
                                <h1><b>WHEEL DEAL</b></h1>
                            </div>
                            <h2>Oops! No Car Data Found, Please Try Again.</h2>
                        </header>
                    </div> 
                </>           
            );
        }
        if(isCars){
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
                                <h3>Price </h3><input type='range' className={node2<5 ? 'low': 'high'} min='0' max='10' step='1' value={node2} onChange={(e)=>setNode2(e.target.value)}/>
                                <h1>{node2}</h1>
                            </div>
                            <div>
                                <h3>Mileage </h3><input type='range' className={node3<5 ? 'low': 'high'} min='0' max='10' step='1' value={node3} onChange={(e)=>setNode3(e.target.value)}/>
                                <h1>{node3}</h1>
                            </div>
                            <div>
                                <h3>Year </h3><input type='range' className={node5<5 ? 'low': 'high'} min='0' max='10' step='1' value={node5} onChange={(e)=>setNode5(e.target.value)}/>
                                <h1>{node5}</h1>
                            </div>
                            <div>
                                <h3>Trim </h3><input type='range' className={node6<5 ? 'low': 'high'} min='0' max='10' step='1' value={node6} onChange={(e)=>setNode6(e.target.value)}/>
                                <h1>{node6}</h1>
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

