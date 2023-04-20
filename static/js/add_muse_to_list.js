'use strict';

// select the hidden museum form
const form = document.getElementById('muse-form');

    let museName = document.querySelector('#detail-muse-name').value;
    let museWebsite =  document.querySelector('#detail-muse-website').value;
    let musePlaceID =  document.querySelector('#detail-place-id').value;
    let musePhone = document.querySelector('#detail-muse-phone');
    let phoneNum = null;

    if (musePhone != null){
        phoneNum = musePhone.value;
    }

// add event listener to the form submission(like button click)
form.addEventListener('submit', evt => {
    // prevent the form from submitting
    evt.preventDefault()

    // gets current museum info the form input values
    const formInputs = {
        name: museName,
        website: museWebsite,
        placeID: musePlaceID,
        phone: phoneNum

    }

     // ajax request to check if there is user in session
    fetch(('/user-session'),{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) =>{

            // hide log in button if user is in session
            // and show log out button and homepage button
            if (responseJson['user_id'] === false){
                alert('Please log in to add museum to your like list.')
            }
        }

    );


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
