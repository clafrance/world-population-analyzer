function countryInfo(country) {

	let url = `/country_info/${country}`;

	d3.json(url).then(function(data) {

		// Select the panel with id of `#country-metadata`
		var panel = d3.select("#country-metadata");

		// Clear any existing metadata
    panel.html("");

    var div = panel.append("div");
    Object.entries(data).forEach(function([key, value]) {
      if (!value) {
        div.append("p").text(`${key}: N/A`);
      } else {
        div.append("p").text(`${key}: ${value}`);
      }    	
    });


    //// Call some function to build chart
	});
}

// Function to build new charts when select a sample value
function optionChanged(newSample) {
  // buildCharts(newSample);
  // buildMetadata(newSample);
}

// // Function to initilize the page
// function init() {

// 	var selector = d3.select("#selCountry");

// 	d3.json("/countries").then((countries) => {
// 		countries.forEach((country) => {
// 			selector
// 				.append("option")
// 				.text(country)
// 				.property("value", country);
// 		});

// 		// // Use the first country from the list to build the initial plots
//   //   const firstCountry = countries[0];
//   //   buildCharts(firstCountry);
//   //   buildMetadata(firstCountry);
// 	});
// }








function countryInfo(country) {

	let url = `/country_info/${country}`;

}


init();
