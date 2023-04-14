'use strict';

// get the user's input password from the form
const input_password = document.querySelector('#acct-password');

// add a event listener on the password input field
// the password requirements div will show when user click on the password input field
input_password.addEventListener('click', ()=>{
    var div = document.querySelector('#password-requirements');

    div.style.display = 'block';
})

// function that validate if the inputted password has meet the requirement
function validatePassword(password){

    const specialChar = ["&", "%", "$", "#", "!"]

    let hasMinLength = false;
    let hasUppercase = false;
    let hasSpecialChar = false;

    if (password.length >= 8){
        hasMinLength = true;
    }

    for(let i = 0; i < password.length; i++){
        if(password[i] === password[i].toUpperCase()){
            hasUppercase = true;
        }
    }

    for(let i = 0; i < password.length; i++){
        if(specialChar.includes(password[i])){
            hasSpecialChar = true;
        }
    }

    return hasMinLength && hasUppercase && hasSpecialChar;
}

// select the create account form
const form = document.querySelector('#create-account-form');

// add event listener on the form that listen to form submission
form.addEventListener('submit', (evt) =>{

    // check if the input password met the password requirement
    // prevent the form subission if the input password doesn't meet the requirement
    if (validatePassword(input_password.value) == false){
        evt.preventDefault()

        // select the div that shows password not met msg
        var div = document.querySelector('#invalid-password');

        // show the msg if password is not met
        if(div.style.display == 'none'){
            div.style.display = 'block';
        }else{
            div.style.display = 'none';
        }
    }
});
