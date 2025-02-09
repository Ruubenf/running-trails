// Initialize leaflet map

var map = new L.Map('leaflet', {
	layers: [
		new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			'attribution': 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
		})
	],
	center: [38.727897, -9.164737],
	zoom: 14
});

// Initialize sidebar
var sidebar = L.control.sidebar('sidebar', {position: 'left'});
map.addControl(sidebar);

sidebar.show();

let trailLayers = {};  // Store trail geometry as leaflet layers

// Fetch top 3 longest trails from API
fetch('http://localhost:5000/best_trails')
    .then(response => response.json())  // Convert API response to JSON
    .then(data => {
        console.log("API Response:", data);  // Prints data in the devtools console

        // Update trail names and distances in the frontend
        if (data.length >= 3) {
            document.getElementById("trail1Name").textContent = data[0].name;
            document.getElementById("trail1Score").textContent = data[0].score;
            document.getElementById("trail2Name").textContent = data[1].name;
            document.getElementById("trail2Score").textContent = data[1].score;
            document.getElementById("trail3Name").textContent = data[2].name;
            document.getElementById("trail3Score").textContent = data[2].score;
        }

        // Make trails clickable
        document.getElementById("trail1Name").addEventListener("click", function () {
            showTrailOnMap(data[0], "red");
        });
        document.getElementById("trail2Name").addEventListener("click", function () {
            showTrailOnMap(data[1], "red");
        });
        document.getElementById("trail3Name").addEventListener("click", function () {
            showTrailOnMap(data[2], "red");
        });
    })
    .catch(error => {
        console.error("Error fetching top trails:", error);
    });

// Get closest trails from API
// 1. Get user location
navigator.geolocation.getCurrentPosition(position => {
    fetch(`http://localhost:5000/trails/location?lat=${position.coords.latitude}&lon=${position.coords.longitude}&epsg=4326`)
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);

        // Update trail names and distances in the frontend
        if (data.length >= 3) {
            document.getElementById("closestTrail1Name").textContent = data[0].name;
            document.getElementById("closestTrail2Name").textContent = data[1].name;
            document.getElementById("closestTrail3Name").textContent = data[2].name;
        }

        for (let i = 0; i < 3; i++) {
            data[i]["id_trail"] = data[i].id_0;
        }

        // Make trails clickable
        document.getElementById("closestTrail1Name").addEventListener("click", function () {
            showTrailOnMap(data[0], "red");
        });
        document.getElementById("closestTrail2Name").addEventListener("click", function () {
            showTrailOnMap(data[1], "red");
        });
        document.getElementById("closestTrail3Name").addEventListener("click", function () {
            showTrailOnMap(data[2], "red");
        });
    })
})

// Show a trail on the map
function showTrailOnMap(trail, color) {
    if (!trail.geometry) {
        console.error("No geometry available for this trail.");
        return;
    }

    // Convert geometry from text to a GeoJSON object
    let trailLayer = L.geoJSON(JSON.parse(trail.geometry), {
        style: { color: color, weight: 4 }
    });

    // Remove previous layers
    map.eachLayer(layer => {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });

    // Remove previous trail description
    let closeButton = document.getElementById("closeButton")
    if (closeButton) {
        closeButton.click();
    }

    // Add the new trail and zoom to it
    trailLayer.addTo(map);
    map.fitBounds(trailLayer.getBounds(), { padding: [50, 50] });
    
    // Add trail description to the sidebar

    // 1. Create trail description
    let trailDescription = document.createElement("div");
    trailDescription.innerHTML = `
    <h3>${trail.name}</h3>
    <p>${trail.descript}</p>
    <h4>Reviews</h4>
    <p>${trail.score} / 5 ⭐</p>
    <span id="closeButton" class="clickable">Close</span>
    `;
    trailDescription.id = "trailDescription";

    // 2. Append trail description to the sidebar
    var sidebar = document.getElementById("sidebar");
    sidebar.appendChild(trailDescription);

    // 3. Add close button functionality
    document.getElementById("closeButton").addEventListener("click", function () {
        sidebar.removeChild(trailDescription);
    });

    // 4. Get comments from the API
    getComments(trail.id_trail);
}

// Get comments from the API
function getComments(trailId) {
    fetch(`http://localhost:5000/trail/${trailId}/comments`)
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);

            // 5. Add comments to the trail description
            if (data.length === 0) {
                return;
            }
            let commentPane = document.createElement("div");
            trailDescription.appendChild(commentPane);
            for (let comment of data) {
                let commentElement = document.createElement("p");
                commentElement.textContent = `${comment.text} - ${comment.score} / 5 ⭐`;
                commentPane.appendChild(commentElement);
            }
        })
        .catch(error => {
            console.error("Error fetching comments:", error);
        });
}