# Carcow
## Scrape (make, model, year, zipcode)
The Scraping Algorithm - An algorithm that receives a car sales website as input, as well as a specific car’s description (make, model, year, zip code), and will scrape that website to find the most similar car within a specified mile radius. The make has to match and the model can partially match (v6 vs v8; This information refers to quality of the car engine, with v8 being a higher producer of horsepower). The results will organize the results by similar colors first, followed by the  closest mileage to the search parameters. The algorithm outputs a list of cars that are most similar to the car staged as input.
</br>Current Version: v1
 </br>  This version takes in a cars description and inputs it into a cars.com search url template. The function then uses BeautifulSoupAPI to parse throug the HTML of the site and then collect the car's price and milage into a CSV file. The program only outputs the first 20 cars.
