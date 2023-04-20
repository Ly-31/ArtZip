'use strict';

// get the create account form and form inputs
const account_form = document.getElementById('create-account-form');

const inputFirstName = document.querySelector('#acct-fname');
const inputLastName = document.querySelector('#acct-lname');
const inputPassword = document.querySelector('#acct-password');
const inputPhone = document.querySelector('#acct-phone');
const inputZipcode = document.querySelector('#acct-zipcode');

// function that check if input first name is empty
function validateFirstName(firstName){

    if (firstName.length === 0){
        return false;
    }
    return true;
}

// function that check if input last name is empty
function validateLirstName(firstLame){

    if (firstLame.length === 0){
        return false;
    }
    return true;
}

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

// function that validate phone number
function validatePhone(phone){
    pass
}

// function that validate zipcode
function validateZipcode(zipcode){
    console.log('validate zipcode')
    if (zipcode.value.length === 5){
        try {
            parseInt(zipcode.value, 10);
            return true;
        }
        catch(error){
            // var div = document.getElementById('invalid-zipcode');
            // div.style.display = 'block';
            console.log(error);
            return false;
        }
    } else {
        return false;
    }
}

// add a event listener on the password input field
// the password requirements div will show when user click on the password input field
inputPassword.addEventListener('click', ()=>{
    var div = document.querySelector('#password-requirements');

    div.style.display = 'block';
})

// add a event listener on the form that checks validates form infos
account_form.addEventListener('submit', (evt) =>{

    // // check if the first name is valid
    // if (validateFirstName(inputFirstName.value) === false){
    //     evt.preventDefault();

    //     // select the div that shows fname not met msg
    //     var div = document.querySelector('#invalid-fname');

    //     // show the msg if first name is invalid
    //     if(div.style.display == 'none'){
    //         div.style.display = 'block';
    //     }
    //     div.style.display == 'none';
    // }

    // // check if the last name is valid
    // if (validateLirstName(inputLastName.value) === false){
    //     evt.preventDefault();

    //     // select the div that shows lname not met msg
    //     var div = document.querySelector('#invalid-lname');

    //     // show the msg if last name is invalid
    //     if(div.style.display == 'none'){
    //         div.style.display = 'block';
    //     }else{
    //         div.style.display == 'none';
    //     }
    // }

    // check if the input password met the password requirement
    // prevent the form subission if the input password doesn't meet the requirement
    if (validatePassword(inputPassword.value) == false){
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

    // check if user enter a zipcode

    if (inputZipcode.value.length !== 0){
        console.log(inputZipcode.value);
        if (validateZipcode(inputZipcode.value) === false){
            evt.preventDefault();

            var div = document.getElementById('invalid-zipcode');
            div.style.display = 'block';
        }
    }
});
