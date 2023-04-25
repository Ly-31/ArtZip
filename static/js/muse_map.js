'use strict';

let placeLat = document.getElementById('lat').innerText;
let placeLng = document.getElementById('lng').innerText;
let placeName = document.getElementById('muse-name').innerText;


function initMap() {
    const museCord = {
        lat: parseFloat(placeLat),
        lng: parseFloat(placeLng),
    };

    const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: museCord,
        zoom: 19,
    });

    const sfMarker = new google.maps.Marker({
        position: museCord,
        title: placeName,
        map: basicMap,
    });

    sfMarker.addListener('click', () => {
        const sfInfo = new google.maps.InfoWindow({
            content: `<h5>${placeName}</h1>`,
    });

    sfInfo.open(basicMap, sfMarker);
    });
};
