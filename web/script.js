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

// Fetch max distance from API
fetch('http://localhost:5000/max_distance')  // ✅ Ensure the correct API URL
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);  // ✅ Debugging: Check API response in browser console
        if (data.max_distance !== null && data.max_distance !== undefined) {
            document.getElementById("maxDistance").textContent = data.max_distance.toFixed(2);
        } else {
            document.getElementById("maxDistance").textContent = "No data available";
        }
    })
    .catch(error => {
        console.error("Error fetching max distance:", error);
        document.getElementById("maxDistance").textContent = "Unavailable";
    })