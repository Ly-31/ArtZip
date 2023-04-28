'use strict';

// get the buttons that show password
const btn_1 = document.getElementById("show-input-pwd1");
const btn_2 = document.getElementById("show-input-pwd2");

// get users password input fields
const pwd1 = document.getElementById("newPwd-1");
const pwd2 = document.getElementById("newPwd-2");

// function that change the input type
function showPwd(pwd){
    console.log("showPWD function called")
    if (pwd.type === "password"){
        pwd.type = "text";
    }else{
        pwd.type = "password";
    }
}

// add event listener to buttons to show the password
btn_1.addEventListener('click', ()=>{
    showPwd(pwd1)
});

btn_2.addEventListener('click', ()=>{
    showPwd(pwd2)
});
