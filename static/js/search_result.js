'use strict';

const loadMoreBtn = document.getElementById('load-more-btn');
loadMoreBtn.addEventListener('click', loadMoreResults);

const googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8';

// Define the loadMoreResults function
function loadMoreResults() {
  // Get the next page token from the button value
    const nextPageToken = loadMoreBtn.value;

    // Make an AJAX request to the Places API
    fetch(`https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=${googlemap_key}&pagetoken=${nextPageToken}`)
        .then(response => response.json())
        .then(data => {
        // Get the places data from the AJAX response
        const placesData = data.results;

        // Create a new HTML element to hold the new results
        const newResultsContainer = document.createElement('div');

        // Loop through the places data and create new HTML elements for each result
        placesData.forEach(place => {
            const placeElement = document.createElement('div');
            placeElement.innerHTML = `
            <div>
                <img src="https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${googlemap_key}" alt="">
                <div>
                <a href="/muse-details?place_id=${place.place_id}">${place.name}</a>
                </div>
                <div>Rating: ${place.rating}</div>
                <br>
                <br>
            </div>
            `;
            newResultsContainer.appendChild(placeElement);
        });

        // Get the container element for the existing results
        const resultsContainer = document.getElementById('results-container');

        // Append the new results to the existing ones
        resultsContainer.appendChild(newResultsContainer);

        // Check if there is a next page token
        if (data.next_page_token) {
            // If there is, update the button value with the new token
            loadMoreBtn.value = data.next_page_token;
        } else {
            // If there is no next page token, hide the button
            loadMoreBtn.style.display = 'none';
        }
        })
        .catch(error => console.error(error));
    }
