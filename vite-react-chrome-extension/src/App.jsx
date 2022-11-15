import React, { useEffect, useState } from 'react';
import './App.css';
import $ from "jquery";
import axios from 'axios';


function App() {
  const [urlCall, setUrl] = useState('');
  const [isCars, setIsCars] = useState(false);

  const [error, setError] = useState(null);
  const [carData, setCarData] = useState(null);
  /**
   * Get current URL
   */
  const conditions = ['cars.com/vehicledetail', 'cargurus.com/Cars/inventorylisting/', 'autotrader.com/cars-for-sale/vehicledetails', 'carsdirect.com/used_cars/vehicle-detail', 'edmunds.com']

  useEffect(() => {
      const queryInfo = {active: true, lastFocusedWindow: true};

      chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
          const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
          setUrl(urlCall); //set url and reset state
          if(conditions.some(element => urlCall.includes(element))){ //check if website is valid (potential edge case if website is something like cars.com.google.com)
            setIsCars(true) //set isCars to true
          }
            console.log("new version");
            // let parsedURL2 = urlCall.replace(/\//g, 'slash').replace(/\./g, 'dot').replace(/:/g, 'colon')
            const parsedURL2 = "just_blank"
            console.log(urlCall)
            console.log(parsedURL2)
            const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL2;
            console.log(fetchURL)
            axios.get(fetchURL)
                .then((response) => {
                    setCarData(response.data);
                    setError(null);                
                    console.log("json test")
                    console.warn(xhr.responseText)
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
              <p>CARCOW</p>
              
              <p>URL:</p>
              <p>
                  {urlCall}
              </p>
              <br/>
              <p>
                  {isCars ? 
                  'Valid Website'
                  : 
                  'Not Valid Website'}
              </p>
              <table border="1">
                    {carData.map(car=>(
                    <tr>
                      <td>
                          <ul>
                              <li>Make: {car.Make}</li>
                              <li>Model: {car.Model}</li>
                              <li>Year: {car.Year}</li>
                              <li>Mileage: {car.Mileage}</li>
                              <li>Price: {car.Price}</li>
                              <a href = {car.url} >URL: Car Page</a>
                          </ul>
                      </td>
                    </tr>  
                    ))}      
              </table>
          </header>
      </div>
  );
};

export default App
