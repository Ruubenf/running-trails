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
                    menu.style.display = "none";
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

//Details of tre selected trail
document.addEventListener("DOMContentLoaded", function () {
    const reviewSection = document.querySelector(".comments"); 
    const reviewText = document.getElementById("trailTitle");
    const closestTrailItems = document.querySelectorAll(".sub-menu .clickable");
    const menuLinks = document.querySelectorAll(".menu-links > li.nav-link > a");
    
    reviewSection.style.display = "none";

    function handleTrailClick(event) {
        const trailName = event.target.textContent;
        reviewText.innerHTML = `<b>Details for ${trailName}</b>`;
        reviewSection.style.display = "block";
        
        fetch("http://localhost:5000/trails")
            .then(response => response.json())
            .then(data => {
                const trail = data.find(t => t.name === trailName);
                if (trail) {
                    document.getElementById("trailDescript").innerHTML = trail.descript;
                    document.getElementById("trailDistance").innerHTML = `<b>Distance:</b> ${trail.distance_m} meters`;
                    document.getElementById("trailSlopemax").innerHTML = `<b>Max Slope:</b> ${trail.slope_max}°`;
                    document.getElementById("trailSlope").innerHTML = `<b>Average Slope:</b> ${trail.slope_mean}°`;
    
                    fetchComments(trail.id_0);
                } else {
                    document.getElementById("trailDescript").textContent = "No description available.";
                    document.getElementById("trailDistance").textContent = "No description available.";
                    document.getElementById("trailSlopemax").textContent = "No description available.";
                    document.getElementById("trailSlope").textContent = "No description available.";
                }
            })
            .catch(error => {
                console.error("Error fetching trails:", error);
                document.getElementById("trailDescript").textContent = "Failed to load description.";
                document.getElementById("trailDistance").textContent = "Failed to load description.";
                    document.getElementById("trailSlopemax").textContent = "Failed to load description.";
                    document.getElementById("trailSlope").textContent = "Failed to load description.";
            }); 
    }

    function fetchComments(trailId) {
        fetch(`http://localhost:5000/trail/${trailId}/comments`)
            .then(response => response.json())
            .then(comments => {
                console.log("Received comments:", comments);
                const commentsContainer = document.getElementById("trailComments"); 

                if (comments.length > 0) {
                    commentsContainer.innerHTML = "<ul>" + comments
                        .map(comment => {
                            let stars = "⭐".repeat(comment.score);
                            return `
                            <b>${comment.runner}</b> <span class="stars">${stars}</span> <p>${comment.text}</p>`;
                        })
                        .join("") + "</ul>";
                } else {
                    commentsContainer.innerHTML = "No reviews available.";
                }
            })
            .catch(error => {
                console.error("Error fetching comments:", error);
                document.getElementById("trailComments").textContent = "Failed to load reviews.";
            });
    }

    function hideReviewSection() {
        reviewSection.style.display = "none";
    }

    closestTrailItems.forEach(item => {
        item.addEventListener("click", handleTrailClick);
    });
    
    menuLinks.forEach(link => {
        link.addEventListener("click", hideReviewSection);
    });
})

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

        // Make Top Trails clickable
        document.getElementById("trail1Name").addEventListener("click", function () {
            showTrailOnMap(data[0], "red", "top");
        });
        document.getElementById("trail2Name").addEventListener("click", function () {
            showTrailOnMap(data[1], "red", "top");
        });
        document.getElementById("trail3Name").addEventListener("click", function () {
            showTrailOnMap(data[2], "red", "top");
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

        // Make Closest Trails clickable
        document.getElementById("closestTrail1Name").addEventListener("click", function () {
            showTrailOnMap(data[0], "red", "closest");
        });
        document.getElementById("closestTrail2Name").addEventListener("click", function () {
            showTrailOnMap(data[1], "red", "closest");
        });
        document.getElementById("closestTrail3Name").addEventListener("click", function () {
            showTrailOnMap(data[2], "red", "closest");
        });
    })
})

// Show a trail on the map
function showTrailOnMap(trail, color, section) {
    
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

    // Add the new trail and zoom to it
    trailLayer.addTo(map);
    map.fitBounds(trailLayer.getBounds(), { padding: [50, 50] });

    currentTrailID = trail.id_trail;

}

// Search trail by Name
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".search-box input");

    const searchBox = document.querySelector(".search-box");
    searchBox.style.position = "relative";

    searchInput.addEventListener("input", function () {
        // Delete previous results
        let searchResults = document.getElementById("searchResults");
        if (searchResults) {
            searchResults.remove();
        }

        const query = searchInput.value.trim();

        fetch(`http://localhost:5000/trails/search?name=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error en la API");
                }
                return response.json();
            })
            .then(data => {
                console.log("API Response:", data);

                // Results box
                searchResults = document.createElement("div");
                searchResults.id = "searchResults";
                searchResults.style.backgroundColor = "white";
                searchResults.style.border = "1px solid #ccc";
                searchResults.style.borderRadius = "6px";
                searchResults.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.15)";
                searchResults.style.padding = "10px";
                searchResults.style.maxHeight = "300px";
                searchResults.style.overflowY = "auto";
                searchResults.style.position = "absolute";
                searchResults.style.top = "100%";
                searchResults.style.left = "0";
                searchResults.style.width = "90%";
                searchResults.style.zIndex = "1000";
                searchResults.style.marginTop = "5px";

                if (data.length === 0) {
                    searchResults.innerHTML = "<p style='margin: 0; padding: 5px;'>No results found</p>";
                } else {
                    for (let trail of data) {
                        let trailElement = document.createElement("p");
                        trailElement.textContent = trail.name;
                        trailElement.classList.add("clickable");
                        trailElement.style.cursor = "pointer";
                        trailElement.style.margin = "8px 0";
                        trailElement.style.padding = "6px";
                        trailElement.style.borderRadius = "5px";
                        trailElement.style.transition = "background-color 0.3s, color 0.3s";

                        trailElement.addEventListener("mouseover", function () {
                            trailElement.style.backgroundColor = "#f4f4f4";
                            trailElement.style.color = "#0f5f04";
                        });
                        trailElement.addEventListener("mouseout", function () {
                            trailElement.style.backgroundColor = "";
                            trailElement.style.color = "";
                        });

                        trailElement.addEventListener("click", function () {
                            showTrailOnMap(trail, "red");
                            searchResults.remove();
                        });

                        searchResults.appendChild(trailElement);
                    }
                }
                searchBox.appendChild(searchResults);
            })
            .catch(error => {
                console.error("Error fetching search results:", error);
            });
    });
    document.addEventListener("click", function (event) {
        let searchResults = document.getElementById("searchResults");
        if (searchResults && !searchBox.contains(event.target)) {
            searchResults.remove();
        }
    });
});

function submitReview() {
    // Get values from the review form
    let runner = document.getElementById("reviewRunner").value;
    let score = document.getElementById("reviewScore").value;
    let text = document.getElementById("reviewText").value;

    // Ensure required fields are not empty
    if (!runner || !score || !text) {
        alert("All fields are required.");
        return;
    }

    let reviewData = {
        id_trail: currentTrailID,  // The trail being reviewed
        runner: runner,  // The name of the person submitting the review
        score: parseInt(score),  // Convert score to integer
        text: text  // The review text
    };

    console.log("Review Data to Send:", reviewData); // Debugging line

    // Send data to the API
    fetch("http://localhost:5000/submit_review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(reviewData)  // Convert object to JSON
    })
    .then(response => response.json())  // Parse the API response
    .then(data => {
        console.log("Review submission response:", data);

        // Clear the form after submission
        document.getElementById("reviewForm").reset();

    })
    .catch(error => {
        console.error("Error submitting review:", error);
    });
}

// Handle score (stars) selection
document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const scoreInput = document.getElementById("reviewScore");

    stars.forEach(star => {
        star.addEventListener("click", function () {
            let rating = this.getAttribute("data-value");
            scoreInput.value = rating;

            // Update star colors
            stars.forEach(s => {
                s.classList.toggle("selected", s.getAttribute("data-value") <= rating);
            });
        });
    });
});

// Create trail
let startingPoint,
    endingPoint,
    startingMarker = null,
    endingMarker = null;

let newStartingPoint = document.getElementById("newStartingPoint");
newStartingPoint.addEventListener("click", function () {

    startingPoint = null;

    if (startingMarker){
        map.removeLayer(startingMarker);
        startingMarker = null;
    }

    map.on("click", function (event) {
        if (!startingPoint){
            startingMarker = L.marker(event.latlng).addTo(map);
            newStartingPoint.value = `${event.latlng.lat}, ${event.latlng.lng}`;
            startingPoint = event.latlng;
        }        
    });
});

let newEndingPoint = document.getElementById("newEndingPoint");
newEndingPoint.addEventListener("click", function () {

    endingPoint = null;

    if (endingMarker){
        map.removeLayer(endingMarker);
        endingMarker = null;
    }

    map.on("click", function (event) {
        if (!endingPoint){
            endingMarker = L.marker(event.latlng).addTo(map);
            newEndingPoint.value = `${event.latlng.lat}, ${event.latlng.lng}`;
            endingPoint = event.latlng;
        }        
    });
});

let calculateBtn = document.getElementById("calculateTrail");
calculateBtn.addEventListener("click", function(){
    let greenPriority = document.getElementById("greenAreasPriority").value;
    fetch(`http://localhost:5000/trail/create?starting=${newStartingPoint.value}&ending=${newEndingPoint.value}&green_priority=${greenPriority/10}`)
    .then(response => response.json())
    .then(trail =>{
        //showTrailOnMap(trail, "red");
        let trailLayer = L.geoJSON(trail.geometry, {
            style: { color: "red", weight: 4 }
        });

        trailLayer.addTo(map);
    });
});