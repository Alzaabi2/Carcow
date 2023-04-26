// import "./M.csv"
import makes from './M.json' assert { type: "json" };
import models from './MM.json' assert { type: "json" };
import trims from './MMT.json' assert { type: "json" };
import axios from 'axios';
import cheerio from 'cheerio';


// function checkMakesInText(text) {
//     // Read the makes CSV file
//     const xhr = new XMLHttpRequest();
//     xhr.open('GET', 'M.csv', false);
//     xhr.send();
//     const makesCSV = xhr.responseText;
//     print(makesCSV)
  
//     // Split the CSV into an array of makes
//     const makes = makesCSV.split(',');
  
//     // Check if any of the makes are included in the text
//     for (let i = 0; i < makes.length; i++) {
//       if (text.includes(makes[i])) {
//         return true;
//       }
//     }
  
//     return false;
//   }

// checkMakesInText('i took my toyota to the shop')
function findMostSimilarString(text, stringList) {
    let minDistance = Infinity;
    let mostSimilarString = null;
  
    stringList.forEach(string => {
      const distance = calculateLevenshteinDistance(text, string);
  
      if (distance < minDistance) {
        minDistance = distance;
        mostSimilarString = string;
      }
    });
  
    return mostSimilarString;
}

function getEditDistance(a, b) {
    if(a.length === 0) return b.length; 
    if(b.length === 0) return a.length; 
  
    var matrix = [];
  
    // increment along the first column of each row
    var i;
    for(i = 0; i <= b.length; i++){
      matrix[i] = [i];
    }
  
    // increment each column in the first row
    var j;
    for(j = 0; j <= a.length; j++){
      matrix[0][j] = j;
    }
  
    // Fill in the rest of the matrix
    for(i = 1; i <= b.length; i++){
      for(j = 1; j <= a.length; j++){
        if(b.charAt(i-1) == a.charAt(j-1)){
          matrix[i][j] = matrix[i-1][j-1];
        } else {
          matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, // substitution
                                  Math.min(matrix[i][j-1] + 1, // insertion
                                           matrix[i-1][j] + 1)); // deletion
        }
      }
    }
  
    return matrix[b.length][a.length];
  };

function calculateLevenshteinDistance(a, b){
    const aLimit = a.length + 1;
    const bLimit = b.length + 1;
    const distance = Array(aLimit);
    for (let i = 0; i < aLimit; ++i) {
        distance[i] = Array(bLimit);
  }
  for (let i = 0; i < aLimit; ++i) {
        distance[i][0] = i;
  }
  for (let j = 0; j < bLimit; ++j) {
        distance[0][j] = j;
  }
  for (let i = 1; i < aLimit; ++i) {
      for (let j = 1; j <  bLimit; ++j) {
          const substitutionCost = (a[i - 1] === b[j - 1] ? 0 : 1);
            distance[i][j] = Math.min(
              distance[i - 1][j] + 1,
              distance[i][j - 1] + 1,
              distance[i - 1][j - 1] + substitutionCost
          );
      }
  }
    return distance[a.length][b.length];
};

function levenshteinDistance(s, t) {
    const d = [];
  
    for (let i = 0; i <= s.length; i++) {
      d[i] = [i];
    }
  
    for (let j = 0; j <= t.length; j++) {
      d[0][j] = j;
    }
  
    for (let j = 1; j <= t.length; j++) {
      for (let i = 1; i <= s.length; i++) {
        if (s[i - 1] === t[j - 1]) {
          d[i][j] = d[i - 1][j - 1];
        } else {
          d[i][j] = Math.min(
            d[i - 1][j] + 1, // deletion
            d[i][j - 1] + 1, // insertion
            d[i - 1][j - 1] + 1 // substitution
          );
        }
      }
    }
  
    return d[s.length][t.length];
}

async function findMakeModel(url){
    const MM = await axios.get(url)
    .then((response) => {
        var $ = cheerio.load(response.data);
        var text = $('title').text()
        var body = $('body').html()
        console.log
        var ret = {}
        ret['body'] = body
        for (var make of models){
            // console.log(make['make'])
            if(text.toLowerCase().includes(make['make'].toLowerCase()) == true){
                ret['make'] = make['make'].toLowerCase()
                if(text.toLowerCase().includes(make['model'].toLowerCase()) == true){
                    ret['model'] = make['model'].toLowerCase()
                    return ret
                }
            }
        }
        return null
    });

    return MM
}

async function findElements(url){
    const MM = await axios.get(url)
    .then((response) => {
        var $ = cheerio.load(response.data);
        var text = $('title').text()
        var body = $('body').html()
        console.log
        var ret = {}
        ret['body'] = body
        for (var make of models){
            // console.log(make['make'])
            if(text.toLowerCase().includes(make['make'].toLowerCase()) == true){
                ret['make'] = make['make'].toLowerCase()
                if(text.toLowerCase().includes(make['model'].toLowerCase()) == true){
                    ret['model'] = make['model'].toLowerCase()
                    return ret
                }
            }
        }
        
    });

    return MM
}

async function findMakeModelTrim(url){
    const car = await findMakeModel(url);
    if(car == null){return null}
    var make = car['make']
    var model = car['model']
    var text = car['body']
    var t = []
    for (var mo of trims){
        // console.log(mo)
        if(mo['make'].toLowerCase() == make && mo['model'].toLowerCase() == model){
            var str = mo['make'] + ' ' + mo['model'] + ' ' + mo['trim']
            t.push(str)
            // console.log(str)
        }
    }
    for (var mo of t){
        if(text.includes(t['trim']) == true){console.log(t['trim'])}
    }
    // console.log(t)
    // var mostSimilarTrim = findMostSimilarString(text, t)
    // if (mostSimilarTrim != null){return mostSimilarTrim}
    // else {return (car['make'] + ' ' + car['model'])}
}
// const text = 'Cars.com Cars for Sale Research & Reviews News & Videos Sell Your Car Service & Repair Menu Home Cars for Sale Search Results New 2023 Toyota Corolla LE Photo of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota CorollaPhoto of 2023 Midnight Black Metallic Toyota Corolla Photo of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Black Metallic Toyota CorollaThumbnail of 2023 Midnight Bl© 2023 Cars.com. All rights reserved.';
console.log(await findMakeModelTrim('https://www.cars.com/vehicledetail/f809f544-f481-45b9-947b-d876f21da50e/'))


// console.log(findMake(text));