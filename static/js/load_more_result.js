'use strict';

const loadMoreBtn = document.getElementById('load-more-btn');
loadMoreBtn.addEventListener('click', loadMoreResults);

const googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8';

function loadMoreResults() {
    const token = loadMoreBtn.value;

    fetch(`/load-more-results.json?token=${token}`)
        .then(response => response.json())
        .then(data => {

        const placesData = data.results;

        const newResultsContainer = document.createElement('div');
        newResultsContainer.classList.add('row')

        placesData.forEach(place => {
            const placeElement = document.createElement('div');
            placeElement.classList.add('col-4')
            let imgUrl;
            if (place.photos && place.photos[0]) {
                imgUrl = `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${googlemap_key}`;
            } else {
                imgUrl = '/static/img/muse.png';
            }

            placeElement.innerHTML = `
                <div>
                    <img class="muse-img" src="${imgUrl}" alt="">
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

        const resultsContainer = document.getElementById('results-container');

        resultsContainer.appendChild(newResultsContainer);

        // If there is a new token, update the button value with the new token
        if (data.next_page_token) {
            loadMoreBtn.value = data.next_page_token;
        } else {
            // If there is no next page token, hide the button
            loadMoreBtn.style.display = 'none';
        }
        })
        .catch(error => console.error(error));
    }
