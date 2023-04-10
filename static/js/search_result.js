'use strict';

const button= document.getElementById("load-more-results")
let token = 


form.addEventListener('submit', (evt) =>{
    evt.preventDefault();
    loadData(inputZipcode);
})

function loadData(inputZipcode){
    console.log(inputZipcode);

    let message = document.querySelector("#zipcode-message");

    if(validateZipcode(inputZipcode) === false){
        // evt.preventDefault()
        message.innerText = "Invalid zipcode";
    }else{

        message.innerText = "Valid zipcode";

        geocodeZip(inputZipcode)
            .then(({lat, lng}) => {
                message.innerText = "Valid zipcode";
                initMap(lat, lng);
            })
            .catch((error) => {
                console.log(error)
                message.innerText = "Unable to find museums for zipcode"
            });

        // initMap();
    }
}


function geocodeZip(zipcode){
    return new Promise((resolve, reject) => {
        const geocoder = new google.maps.Geocoder()
        geocoder.geocode({address:zipcode}, (results, status) => {
            if (status === "OK"){
                const lat = results[0].geometry.location.lat();
                const lng = results[0].geometry.location.lng();
                console.log(`lat${lat} lng${lng}`)
                resolve({lat, lng});
            } else if (status === "ZERO_RESULTS"){
                console.log("Zero result found")
                reject("Zero results found")
            } else {
                console.log("Not a valid zipcode")
                reject("Not a valid zipcode")
            }
        })
    })

}


function initMap(lat, lng) {
    // Create the map.

    const center = {lat: lat, lng: lng };
    const map = new google.maps.Map(
    document.getElementById("map"),
    {
        center: center,
        zoom: 17,
    }
    );

    // Create the places service.
    const service = new google.maps.places.PlacesService(map);
    let getNextPage;
    const moreButton = document.getElementById("more");

    moreButton.onclick = function () {
    moreButton.disabled = true;

    if (getNextPage) {
        getNextPage();
    }
    };

    // Perform a nearby search.
    service.nearbySearch({
        location: center,
        radius: 50000,
        type: "museum",
        keyword: ["museum", "gallery"]
        },
        function(results, status, pagination){
        if (status !== "OK" || !results) return;

        console.log(results);

        addPlaces(results);
        moreButton.disabled = !pagination || !pagination.hasNextPage;

        if (pagination && pagination.hasNextPage) {
            getNextPage = () => {
            // Note: nextPage will call the same handler function as the initial call
            pagination.nextPage();
        };
        }
    }
    );
}

function addPlaces(places) {
    const placesList = document.getElementById("places");

    for (const place of places) {
        // if (place.geometry && place.geometry.location) {
        //     const image = {
        //     url: place.icon,
        //     size: new google.maps.Size(71, 71),
        //     origin: new google.maps.Point(0, 0),
        //     anchor: new google.maps.Point(17, 34),
        //     scaledSize: new google.maps.Size(25, 25),
        //     };

        const li = document.createElement("li");

        li.textContent = place.name;
        placesList.appendChild(li);

    // }
    }
}

// window.initMap = initMap;
let params = new URLSearchParams(window.location.search);
let zipcode = params.get('search-bar-zipcode')

loadData(zipcode);
