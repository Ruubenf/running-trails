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
map.zoomControl.setPosition("bottomright");

let trailLayers = {};

//Initialize sidebar
const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");

    toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close");
    });


    modeSwitch.addEventListener("click", () =>{
        body.classList.toggle("dark");

        if(body.classList.contains("dark")){
            modeText.innerText = "Light Mode"
        }else{
            modeText.innerText = "Dark Mode"
        }
    });
//Sub-menu
document.addEventListener("DOMContentLoaded", function() {
    const arrows = document.querySelectorAll(".nav-link");

    arrows.forEach(arrow => {
        arrow.addEventListener("click", function() {
            let menuLink = this.closest(".menu-links"); 
            let subMenu = menuLink.querySelector(".sub-menu");

            // Close previous sub-menus
            document.querySelectorAll(".sub-menu").forEach(menu => {
                if (menu !== subMenu) {
                    menu.style.display = "none"; // Oculta otros submenús
                    menu.parentElement.classList.remove("active");
                }
            });

            if (subMenu.style.display === "block") {
                subMenu.style.display = "none";
                menuLink.classList.remove("active");
            } else {
                subMenu.style.display = "block";
                menuLink.classList.add("active");
            }
        });
    });
});

//Top Trails from API
fetch('http://localhost:5000/best_trails')
    .then(response => response.json())  // Convert API response to JSON
    .then(data => {
        console.log("API Response:", data);  // Prints data in the devtools console

        // Update trail names and scores
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

// Closest Trails from API
// Get user location
navigator.geolocation.getCurrentPosition(position => {
    fetch(`http://localhost:5000/trails/location?lat=${position.coords.latitude}&lon=${position.coords.longitude}&epsg=4326`)
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);

        // Update trail names
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
}

//Show reviews on a box
function showReviewBox(trail){
    document.getElementById("trailTitle").innerText= trail.name;
    document.getElementById("reviewBox").style.display = "block"; // Muestra la caja de reseñas
    getComments(trail.id_trail);
}

// Close the review box
function closeCommentBox() {
    document.getElementById("reviewBox").style.display = "none"; // Oculta la caja de reseñas
}





// Función para enviar la reseña (puedes modificarla para enviar datos a una API)
//function submitComment() {
    //let comment = document.getElementById("reviewInput").value;
    //if (comment.trim() === "") {
       // alert("Please write a review before submitting.");
        //return;
   // }
    
   // alert("Review submitted: " + comment);
   // document.getElementById("reviewInput").value = ""; 
    //closeCommentBox();}

