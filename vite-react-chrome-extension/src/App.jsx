import React, { useEffect, useState } from 'react';
import './App.css';
import $ from "jquery";
import axios from 'axios';
//import { Make } from 'make';
// import './topThree.js'

// function split (str, index1, index2){
//     const result = str.slice(index1, index2);
//     return result;
// }

function App() {
  const [urlCall, setUrl] = useState('');
  const [isCars, setIsCars] = useState(false);

  const [contacts, setContacts] = useState([]);
  const [error, setError] = useState(null);
  const [carData, setCarData] = useState('');
  /**
   * Get current URL
   */
  useEffect(() => {
      const queryInfo = {active: true, lastFocusedWindow: true};

      chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
          const urlCall = tabs[0].url.toLowerCase() //convert to lowercase
          setUrl(urlCall); //set url and reset state
          if(urlCall.includes('cars.com/vehicledetail')){ //check if website is cars.com (potential edge case if website is something like cars.com.google.com)
            setIsCars(true) //set isCars to true
          }
          if(urlCall == 'chrome://newtab/')
          {
            console.log("empty call");
            urlCall2 = '328daed2-aa5f-4882-bddc-d0bde3601e15'
            const fetchURL =  '127.0.0.1:8080/getUrl/' + urlCall2;
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
            // const parsedURL = urlCall.replace('https://www.cars.com/vehicledetail/', '')
            console.log(urlCall)
            const parsedURL2 = urlCall.replaceAll('/', 'replaceslashes')
            console.log(parsedURL2)
            const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL2;
            console.log(fetchURL)
            axios.get(fetchURL)
                // .then(res => res.json())
                .then((response) => {
                    //console.log(response.json); 
                    setContacts(response.data);
                    setError(null);
                    console.log(response.data);

                    const carList = JSON.stringify(response.data);
                    //const parsedList = JSON.parse (carList);
                    carList.replace (/^\[(.+)\]$/, '');
                    // carList.replace (']/g', '');
                    // carList.replace ('},/g', '}');
                    const carArr = carList.split('}');

                    for (let i = 0; i < 5; i++){
                        carArr[i].replace (/^\[(.+)\]$/, '');
                    }

                    //const data = JSON.parse(carList.toString());

                    // var sanitized = data.replace(/},{/g,'}{');
                    // var res = JSON.parse(sanitized);

                    // console.log(res);
                    //setCarData(response.json);
                    response.data.forEach((carList) => {
                        console.log(carList['Make'])
                        console.log(carList['Model'])
                        console.log(carList['Price'])
                    });
                    setCarData(carArr)
                    //setCarData(response.data);
                    //console.log(carData)
                })
                // .catch(setError);
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
              <table border="1">
                {/* Original: {carData} */}
                    <tr><td>Car Data 1: {carData[0]}</td></tr>
                    <tr><td>Car Data 2: {carData[1]}</td></tr>
                    <tr><td>Car Data 3: {carData[2]}</td></tr>
                    <tr><td>Car Data 4: {carData[3]}</td></tr>
                    <tr><td>Car Data 5: {carData[4]}</td></tr>           
              </table>
          </header>
      </div>
  );
};

export default App
