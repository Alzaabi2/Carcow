import React, { useEffect, useState } from 'react';
import './App.css';
import $ from "jquery";
import axios from 'axios';
//import { Make } from 'make';
import './App.css'

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
            const parsedURL = urlCall.replace('https://www.cars.com/vehicledetail/', '')
            const parsedURL2 = parsedURL.replace('/', '')
            const fetchURL =  'http://127.0.0.1:8080/getUrl/' + parsedURL2;
            console.log(fetchURL)
            axios.get(fetchURL)
                // .then(res => res.json())
                .then((response) => {
                    //console.log(response.json); 
                    setContacts(response.data);
                    setError(null);
                    //console.log(response.data);
                    
                    var carStr = JSON.stringify(response.data);
                    // carStr = carStr.replaceAll ('{"Make":"', "");
                    // carStr = carStr.replaceAll ('"Mileage":"', "");
                    //console.log(carStr);
                    var arr = carStr.split('},');
                    //console.log (arr);

                    var finalArr = [];
                    for (let i = 0; i < 5; i++){
                        var singleCar = arr[i].replace("[", "");
                        singleCar = singleCar + '}';
                        //console.log(singleCar);

                        var arr2 = singleCar.split('",');
                        var make = arr2[0].replace('{"Make":"', "");
                        make = make.replace('",', "");

                        var mileage = arr2[1].replace('"Mileage":"', '');
                        mileage = mileage.replace ('"', '');
                        
                        var model = arr2[2].replace('"Model":"','');
                        model = model.replace('"', '');

                        var price = arr2[3].replace('"Price":"', '');
                        price = price.replace ('"', '');
                        price = '$' + price;
                        
                        var year = arr2[4].replace('"Year":"', '');
                        year = year.replace ('"', '');
                        
                        var url = arr2[5].replace('url":"', '');
                        url = url.replace ('"}', '');
                        
                        console.log(make);
                        console.log(model);                   
                        console.log(year);
                        console.log(mileage); 
                        console.log(price);
                        console.log(url);

                        finalArr.push(make);
                        finalArr.push(model);
                        finalArr.push(year);
                        finalArr.push(mileage);
                        finalArr.push(price);
                        finalArr.push(url);
                    }        
                    
                            
                    
                    //var parsedList = JSON.parse (carStr);
                    //carStr.replace (/^\[(.+)\]$/, '');
                    // carStr.replace (']/g', '');
                    // carStr.replace ('},/g', '}');

                    // response.data.forEach((carStr) => {
                    //     console.log(carStr['Make'])
                    //     console.log(carStr['Model'])
                    //     console.log(carStr['Price'])
                    // });

                    //carStr = carStr.split('[{' | '},{');
                    // carStr = carStr.split(',');
                    // carStr = carStr.split (':');

                    // for (let i = 0; i < 40; i++){
                    //     carStr[i].replace (/^\[(.+)\]$/, '');
                    // }

                    //const data = JSON.parse(carStr.toString());

                    // var sanitized = data.replace(/},{/g,'}{');
                    // var res = JSON.parse(sanitized);

                    // console.log(res);
                    //setCarData(response.json);
                    
                    setCarData(finalArr);
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
                  'Valid Website'
                  : 
                  'Not Valid Website'}
              </p>
              <table border="1">
                {/* Original: {carData} */}
                    <tr>
                        <td> Car Data 1
                            <ul>
                                <li>Make: {carData[0]}</li>
                                <li>Model: {carData[1]}</li>
                                <li>Year: {carData[2]}</li>
                                <li>Mileage: {carData[3]}</li>
                                <li>Price: {carData[4]}</li>
                                <li>URL: {carData[5]}</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>Car Data 2
                            <ul>
                                <li>Make: {carData[6]}</li>
                                <li>Model: {carData[7]}</li>
                                <li>Year: {carData[8]}</li>
                                <li>Mileage: {carData[9]}</li>
                                <li>Price: {carData[10]}</li>
                                <li>URL: {carData[11]}</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>Car Data 3
                            <ul>
                                <li>Make: {carData[12]}</li>
                                <li>Model: {carData[13]}</li>
                                <li>Year: {carData[14]}</li>
                                <li>Mileage: {carData[15]}</li>
                                <li>Price: {carData[16]}</li>
                                <li>URL: {carData[17]}</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>Car Data 4
                            <ul>
                                <li>Make: {carData[18]}</li>
                                <li>Model: {carData[19]}</li>
                                <li>Year: {carData[20]}</li>
                                <li>Mileage: {carData[21]}</li>
                                <li>Price: {carData[22]}</li>
                                <li>URL: {carData[23]}</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>Car Data 5
                            <ul>
                                <li>Make: {carData[24]}</li>
                                <li>Model: {carData[25]}</li>
                                <li>Year: {carData[26]}</li>
                                <li>Mileage: {carData[27]}</li>
                                <li>Price: {carData[28]}</li>
                                <li>URL: <a href = {carData[29]} target="_blank">See Car Listing</a></li>
                            </ul>
                        </td>
                    </tr>       
              </table>
          </header>
      </div>
  );
};

export default App
