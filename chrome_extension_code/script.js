async function fetchData() {
    const urlString = window.location.search;
    if (console.log(urlParams.has('www.cars.com'))){
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
}fetchData();