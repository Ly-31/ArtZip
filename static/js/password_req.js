'use strict';

const input_password = document.querySelector('#acct-password');

input_password.addEventListener('click', ()=>{
    var div = document.querySelector('#password-requirements');

    div.style.display = 'block';
})


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


const form = document.querySelector('#create-account-form');


form.addEventListener('submit', (evt) =>{
    console.log(input_password.value)

    if (validatePassword(input_password.value) == false){
        evt.preventDefault()
        var div = document.querySelector('#invalid-password');

        if(div.style.display == 'none'){
            div.style.display = 'block';
        }else{
            div.style.display = 'none';
        }
    }
});
