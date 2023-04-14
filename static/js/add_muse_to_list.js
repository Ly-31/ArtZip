'use strict';

// select the hidden museum form
const form = document.getElementById('muse-form');

// add event listener to the form submission(like button click)
form.addEventListener('submit', evt => {
    // prevent the form from submitting
    evt.preventDefault()

    // gets current museum info the form input values
    const formInputs = {
        name: document.querySelector('#detail-muse-name').value,
        website: document.querySelector('#detail-muse-website').value,
        placeID: document.querySelector('#detail-place-id').value,
        phone: document.querySelector('#detail-muse-phone').value
    }

    // make a ajax post request to /add-to-list route
    // which will add current museum to user liked list 
    fetch(('/add-to-list'), {
        method: "POST",
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) =>{
        alert(responseJson.status);
    })
    .catch(error => console.error(error));

});
