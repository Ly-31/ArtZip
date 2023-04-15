'use strict';


// ajax reques to check if there is user in session
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
        if (responseJson['user_id'] === true){
            const login_link = document.getElementById('login');
            const logout_link = document.getElementById('logout');
            const user_home = document.getElementById('user-homepage');

            login_link.style.display = 'none';
            logout_link.style.display ='block';
            user_home.style.display = 'block';
        }

    })
    .catch(error => console.error(error));
