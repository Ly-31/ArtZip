'use strict';

let slideIndex = 0;

// calls the function to display the first slide when the page loads
showSlides();

// function that shows the slides
function showSlides() {
    let i;

    // gets the slide elements and dot elements
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");

    // loop over slides, and hide the slide
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // increment the slide index by 1
    slideIndex++;

    // if slideIndex > slides lenght, reset the slideIndex to 1
    if (slideIndex > slides.length){slideIndex = 1}

    // loop over the dots, and remove active from class
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    // show the slide that corresponse to the current slide index
    // add active to current dot's class
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";

    // set a timer to call the slide show function every 3 seconds
    setTimeout(showSlides, 3000);
}
