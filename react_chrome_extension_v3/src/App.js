import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

const App = () => {
    const [url, setUrl] = useState('');
    const [isCars, setIsCars] = useState(false);

    /**
     * Get current URL
     */
    useEffect(() => {
        const queryInfo = {active: true, lastFocusedWindow: true};

        chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
            const url = tabs[0].url.toLowerCase() //convert to lowercase
            setUrl(url); //set url and reset state
            if(url.includes('cars.com')){ //check if website is cars.com (potential edge case if website is something like cars.com.google.com)
            setIsCars(true) //set isCars to true
            }
        });

        return () => setIsCars(false) //before next useEffect is created, set isCars to false

    }, [chrome.tabs]);


    return (
        <div className="App">
            <header className="App-header">
                <p>CARCOW</p>
                
                <p>URL:</p>
                <p>
                    {url}
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