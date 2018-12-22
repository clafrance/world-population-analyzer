//function for map";
console.log("Lets Start plot map");

var countries = [];


var myMap = L.map("map", {
  center: [39.91, -77.02],
  zoom: 3
});



L.tileLayer(`https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}`, {
  attribution: `Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>`,
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

function mapPlot(year) {

  let url_map = `/total_population_by_year/${year}`; 

  console.log(url_map);
  d3.json(url_map).then(function(response) {

    var data = response[0];

    data.country.forEach((country, i) => {

      temp_dict = {name: country,
        capital: data.capital[i], 
        location: [data.latitude[i], data.longitude[i]],
        population: data.population[i]};

      countries.push(temp_dict);
    });


    function markerSize() {
      return 100000;
    }

    for (var i = 0; i < countries.length; i++) {
      L.circle(countries[i].location, {
        fillOpacity: 0.75,
        color: "red",
        fillColor: "red",
        radius: 100000
      }).bindPopup("<h2>" + countries[i].name + "</h2> <hr> <h4>Population: " + countries[i].population + " (k)</h4>").addTo(myMap);
    }
  

    console.log(countries);
  });

}

