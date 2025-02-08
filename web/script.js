var map = new L.Map('leaflet', {
	layers: [
		new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			'attribution': 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
		})
	],
	center: [38.727897, -9.164737],
	zoom: 14
});


var sidebar = L.control.sidebar('sidebar', {position: 'left'});
map.addControl(sidebar);

sidebar.show();

// Fetch top 3 longest trails from API
fetch('http://localhost:5000/top_trails')
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);  // Debugging: Check API response in devtools console

        // Ensure there are at least 3 trails
        if (data[0]) {
            document.getElementById("trail1Name").textContent = data[0].name;
            document.getElementById("trail1Distance").textContent = data[0].distance_m.toFixed(2);
        }
        if (data[1]) {
            document.getElementById("trail2Name").textContent = data[1].name;
            document.getElementById("trail2Distance").textContent = data[1].distance_m.toFixed(2);
        }
        if (data[2]) {
            document.getElementById("trail3Name").textContent = data[2].name;
            document.getElementById("trail3Distance").textContent = data[2].distance_m.toFixed(2);
        }
    })
    .catch(error => {
        console.error("Error fetching top trails:", error);
        document.getElementById("trail1Name").textContent = "Unavailable";
        document.getElementById("trail1Distance").textContent = "N/A";
        document.getElementById("trail2Name").textContent = "Unavailable";
        document.getElementById("trail2Distance").textContent = "N/A";
        document.getElementById("trail3Name").textContent = "Unavailable";
        document.getElementById("trail3Distance").textContent = "N/A";
    });