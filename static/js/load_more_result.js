'use strict';


const googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8';


// select the load more button
const loadMoreBtn = document.getElementById('load-more-btn');

// add event listener to the button
loadMoreBtn.addEventListener('click', loadMoreResults);

// make adjx request to /load-more-results route to load the next batch result
// and manipulate the DOM to add those results
function loadMoreResults() {

    // get the next page token from button value
    const token = loadMoreBtn.value;

    // make adjx request to /load-more-results route, which returns json object
    fetch(`/load-more-results.json?token=${token}`)
        .then(response => response.json())
        .then(data => {

        // extract the list of museums datas from the response
        const placesData = data.results;

        // select the result div to add
        const resultsContainer = document.getElementById('results-container');


        // loop over the list of museums, and extract needed datas
        placesData.forEach(place => {
            // create a div for each museum
            const placeElement = document.createElement('div');
            placeElement.classList.add('col-12', 'col-md-6', 'col-lg-4', 'my-4');
            let imgUrl;

            // check if the museum has photo
            if (place.photos && place.photos[0]) {
                imgUrl = `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${googlemap_key}`;
            } else {
                imgUrl = '/static/img/muse.png';
            }

            // add current museum data to the museum div
            placeElement.innerHTML = `
                    <img class="muse-img img-fluid my-2" src="${imgUrl}" alt="">
                    <div>
                    <a href="/muse-details?place_id=${place.place_id}">${place.name}</a>
                    </div>
                    <div>Rating: ${place.rating}</div>
            `;

            // append current museum div to the result div
            resultsContainer.insertAdjacentElement('beforeend', placeElement);
        });

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
