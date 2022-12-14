import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import $ from "jquery";
import axios from 'axios';
//import Contact from './Contact';

const App = () => {
    const [urlCall, setUrl] = useState('');
    const [isCars, setIsCars] = useState(false);

    const [contacts, setContacts] = useState([]);
    const [error, setError] = useState(null);

    /**
     * Get current URL
     */
    useEffect(() => {
        const queryInfo = {active: true, lastFocusedWindow: true};

        chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
            const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(urlCall); //set url and reset state
            if(urlCall.includes('cars.com')){ //check if website is cars.com (potential edge case if website is something like cars.com.google.com)
            setIsCars(true) //set isCars to true
            }
            if(urlCall != '')
            {
            console.log("empty call");
            urlCall = 'https://www.cars.com/vehicledetail/328daed2-aa5f-4882-bddc-d0bde3601e15/'
            const fetchURL =  '127.0.0.1:8080/getUrl/' + urlCall;
            console.log(fetchURL)
            axios (fetchURL)
                .then((response) => {
                    setContacts(response.data);
                    setError(null);
                })
                .catch(setError);
            }
            else {
            console.log("new version");
            const fetchURL =  '127.0.0.1:8080/getUrl/' + urlCall;
            console.log(fetchURL)
            axios (fetchURL)
                .then((response) => {
                    setContacts(response.data);
                    setError(null);
                })
                .catch(setError);
            }
        });
        
        // //add call the url :
        // $.ajax({
        //     type: "POST",
        //     url: "127.0.0.1:8080/getUrl/",
        //     data: { param: urlCall}
        //   }).success(function() {
        //         alert("Car data passed successfully")
        //   }).fail(function() {
        //         alert("Car data not failed to be passed")
        // });
        return () => setIsCars(false) //before next useEffect is created, set isCars to false
        
    //attempt 2 using axios
        // const instance = axios.create();
        // //Set config defaults for the instance
        // instance.defaults.baseURL = "127.0.0.1:8080";
        // //Send requests using the created instance
        // instance.get("/getUrl/example").then(response => {
        //     console.log('getURL');
        // });

    }, [chrome.tabs]);

    if (error) {
        return alert(error)
    }


    return (
        <div className="App">
            <header className="App-header">
                <p>CARCOW</p>
                
                <p>URL:</p>
                <p>
                    {urlCall}
                </p>
                <br/>
                <p>
                    {isCars ? 
                    'Valid'
                    : 
                    'Not Valid Website'}
                </p>
            </header>
        </div>
    );
};

export default App