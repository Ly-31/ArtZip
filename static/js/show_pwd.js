'use strict';

const showBtn = document.getElementById('show-pwd');

showBtn.addEventListener('click', ()=>{
    fetch(('/show-pwd'), {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        }
})
    .then(response => response.json())
    .then(data => {
        const pwdDiv = document.getElementById('current-pwd');
        pwdDiv.innerText = data['pwd']
    });
});
