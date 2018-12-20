// Function to display world info in the panel
function worldInfo() {
	let panel = d3.select("#country-metadata");
	panel.html("");
	let div = panel.append("div");
	div.append("p").attr("class", "bold").text(`Total Population:`);
	div.append("p").text(`1000000000`);

	div.append("p").attr("class", "bold").text(`Female Population:`);
	div.append("p").text(`500000000`);

	div.append("p").attr("class", "bold").text(`Male Population:`);
	div.append("p").text(`500000000`);    
}


// Function to display world info in the panel
function countryInfo(country) {
	let url = `/country_info/${country}`; 

	d3.json(url).then(function(data) {

		// Select the panel with id of `#country-metadata`
		let panel = d3.select("#country-metadata");

		// Clear any existing metadata
    panel.html("");

    let div = panel.append("div");
    Object.entries(data).forEach(function([key, value]) {
      if (!value) {
        div.append("p").text(`${key}: N/A`);
      } else {

      	if (key ===  "Code") {
      		div.append("p").attr("class", "bold").text(`Country ${key}:`);
      	} else {
      		div.append("p").attr("class", "bold").text(`${key}:`);
      	}
      	div.append("p").text(`${value}`);
        // div.append("p").text(`${key}: ${value}`);
      }    	
    });
	});
}


// Function to initilize the page
function init() {

	var selector = d3.select("#selCountry");

	d3.json("/countries").then((countries) => {
		countries.forEach((country) => {
			selector
				.append("option")
				.text(country)
				.property("value", country);
		});

		// Use the first country from the list to build the initial plots
    const world = countries[0];
    worldInfo();

    // Add all build chart function here here:
    // buildCharts(world);
    // buildMetadata(world);
	});
}


// Function to build new charts when select a country
function optionChanged(newCountry) {

  // buildCharts(newSample);
  if (newCountry === "WORLD") {
  	worldInfo();
  } else {
  	countryInfo(newCountry);
  }

}


init();
