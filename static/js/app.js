// function countryInfo(country) {
// 	console.log(country);
// // 	let url = `/country_info/${country}`;

// // 	console.log(country);

// // 	d3.json(url).then(function(data) {

// // 		// Select the panel with id of `#country-metadata`
// // 		let panel = d3.select("#country-metadata");

// // 		cousole.log(panel);

// // 		// Clear any existing metadata
// //     panel.html("");

// //     let div = panel.append("div");
// //     Object.entries(data).forEach(function([key, value]) {
// //       if (!value) {
// //         div.append("p").text(`${key}: N/A`);
// //       } else {
// //         div.append("p").text(`${key}: ${value}`);
// //       }    	
// //     });


// // //     //// Call some function to build chart
// // 	});
// }


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
  //   const firstCountry = countries[0];
  //   buildCharts(firstCountry);
  //   buildMetadata(firstCountry);
	});
}


// Function to build new charts when select a country
function optionChanged(newCountry) {
  // buildCharts(newSample);
  countryInfo(newCountry);
}


init();
