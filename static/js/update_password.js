'use strict';

// show the change password form when the btn is clicked
const btn = document.getElementById('change-pwd-btn');

btn.addEventListener('click', ()=>{
    form.style.display = 'block';
});

// get update password form
const form = document.getElementById('change-pwd');
const form_submit_btn = document.getElementById('submit-pwd-change');



form_submit_btn.addEventListener('click',(evt)=>{

    evt.preventDefault()

    // get user inputted passwords
    const pw1 = document.getElementById('newPwd-1').value;
    const pw2 = document.getElementById('newPwd-2').value;
    const data = {newPwd: pw1}

    // check is new password entry matches
    if (pw1 !== pw2){
        evt.preventDefault();
        alert("Password does not match!");
    }else if(validatePassword(pw1) !== true){
        evt.preventDefault();
        alert("Invalid Password.");
    }else{
        fetch(('/update-password'),{
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((response) => response.json())
        .then((responseJson) => {
            console.log(responseJson.status)
            alert(responseJson.status);

            form.style.display = 'none';
            document.getElementById('newPwd-1').value = '';
            document.getElementById('newPwd-2').value = '';
        })
        .catch(error => console.error(error));
    }
});

