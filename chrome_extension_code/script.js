const chaiAsPromised = require("chai-as-promised");

async function fetchData() {
    const urlString = 'www.cars.com';
    chrome.tabs.query({active: true, currentWindow:
    true}, function(tabs) {
    var tab = tabs[0];
    console.log(tab.url);
    });
    
    if (console.log(urlString)){
        const record = await res.json();
        console.log(record);
        document.getElementById("make").innerHTML=record.data[0].make;
        document.getElementById("model").innerHTML=record.data[0].model;
        document.getElementById("year").innerHTML=record.data[0].year;
        document.getElementById("mileage").innerHTML=record.data[0].mileage;
        document.getElementById("price").innerHTML=record.data[0].price;
    }
    else{

    }
}

fetchData();