'use strict';

// function that check if current museum is liked by user already
function checkLike() {

    // get the like button, current musesum name
    const likeBtn = document.getElementById('add-to-like');
    const currentMuseName = document.getElementById('detail-muse-name').value;
    const museData = {name: currentMuseName}

    // fetch request to back end server to check if user liked this museum
    fetch(('/check-like'),{
        method: 'POST',
        body: JSON.stringify(museData),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        // if user liked current museum, disable the like button
        if (responseJson.liked === true){
            if (likeBtn.hasAttribute('disabled') !== true){
                likeBtn.setAttribute('disabled','disabled');
            }
        }
    })
}

// call the function after all HTML content has been completely parsed.
addEventListener("DOMContentLoaded", () =>{
    checkLike()
})
