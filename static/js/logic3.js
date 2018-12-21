// Creating our initial map object
var myMap = L.map("map", {
  center: [39.91, -77.02],
  zoom: 3
});

// Adding a tile layer (the background map image) to our map
// We use the addTo method to add objects to our map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

// Define a markerSize function that will give each country a different radius based on its population
function markerSize(population) {
  return population / 40;
}

// Each country object contains the country's name, capital's location and population
var countries = [
  {
    name: "Afghanistan",
    capital: "",
    location: [34.28, 69.2],
    population: 8550405
  },
  {
    name: "Canada",
    capital: "",
    location: [45.27, -75.42],
    population: 2720546
  },
  {
    name: "China",
    capital: "Beijing",
    location: [39.55, 116.2],
    population: 2296224
  },
  {
    name: "France",
    capital: "Paris",
    location: [48.5, 2.2],
    population: 3971883
  },
  {
    name: "Hungary",
    capital: "",
    location: [47.29, 19.05],
    population: 446599
  }
];

// Loop through the countries array and create one marker for each country object
for (var i = 0; i < countries.length; i++) {
  L.circle(countries[i].location, {
    fillOpacity: 0.75,
    color: "red",
    fillColor: "red",
    radius: 100000
  }).bindPopup("<h2>" + countries[i].name + "</h2> <hr> <h4>Population: " + countries[i].population + "</h4>").addTo(myMap);
}


console.log("hi");
