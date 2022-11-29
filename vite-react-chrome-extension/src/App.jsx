import React, { useEffect, useState, useRef } from 'react';
import './App.css';
import $ from "jquery";
import axios from 'axios';

function App() {
    const [urlCall, setUrl] = useState('');
    const [isCars, setIsCars] = useState(false);

    const [error, setError] = useState(null);
    const [carData, setCarData] = useState(null);
    /*
     * Get current URL
     */
    //const conditions = ['cars.com/vehicledetail', 'cargurus.com/Cars/inventorylisting/', 'autotrader.com/cars-for-sale/vehicledetails', 'carsdirect.com/used_cars/vehicle-detail', 'edmunds.com']

    useEffect(() => {
        const queryInfo = {active: true, lastFocusedWindow: true};

        chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
            const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(urlCall); //set url and reset state
            if (urlCall.includes('cars.com/vehicledetail')){
                setIsCars(true) //set isCars to true
            }
            // if(conditions.some(element => urlCall.includes(element))){ //check if website is valid (potential edge case if website is something like cars.com.google.com)
            //     setIsCars(true) //set isCars to true
            // }
            
            console.log("new version");
            const parsedURL2 = urlCall.replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colon')
            console.log(urlCall)
            console.log(parsedURL2)
            const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL2;
            console.log(fetchURL)
            axios.get(fetchURL)
                .then((response) => {
                    setCarData(response.data);
                    setError(null);                
                    console.log("json test")
                    // console.warn(xhr.responseText)
                    console.log(response)
                    console.log(response.data[0]['Year'])
                    console.log("json test end")      
                })
            

            
            
        });
      
      return () => setIsCars(false) //before next useEffect is created, set isCars to false
    

    }, [chrome.tabs]);

    if (error) {
        return alert(error)
    }

    if (!carData) return null;

    return (
        <div className="App">
            <header className="App-header">
                <div class="banner">
                    <h1><b>CARCOW</b></h1>
                </div>
                <h2>
                    {isCars ? 
                    'Valid Website'
                    : 
                    'Not Valid Website'}
                </h2><br/>
                    <table border="1">
                        {carData.map(car=>(
                            <tr>
                                <td>
                                    <img src="https://platform.cstatic-images.com/xlarge/in/v2/ba68b77e-18eb-5a53-ae3e-0f4ee3dcf547/8c3800b9-3377-4ab1-a8d2-7bc365242b85/TE9b9NPjC2nkWbiKvQzHSTR0T_w.jpg" alt="Image Not Found"/>
                                </td>
                                <td><a href = {car.url} target="_blank">
                                    <div class="car-basics">{car.Year} {car.Make} {car.Model}</div>{"\n"}
                                    <div class="display-container">
                                        <div class="car-price">{car.Price} </div>&nbsp;<div class="car-mileage"> {car.Mileage}</div>
                                    </div>
                                </a></td>
                            </tr>
                        ))}      
                    </table>
            </header>
        </div>
    );
};

export default App
