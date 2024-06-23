const url = 'http://localhost'

function login(email) {
    const notLogged = document.getElementsByClassName('loggedOut');
    const logged = document.getElementsByClassName('loggedIn');
    const navEmail = document.getElementById('userLogged');

    for(let i = 0; i<notLogged.length; i++){
        notLogged[i].style.display = "none";
    }

    for(let i = 0; i<logged.length; i++){
        logged[i].style.display = "block";
    }
    navEmail.innerHTML = email
}

function logoff() {
    location.reload();
}

// Auth
async function getLogin(){
    const email = document.getElementById('usernameLogin').value;
    const password = document.getElementById('senhaLogin').value;
    const res = await fetch(url + `/auth/${email}&${password}`, {
        method: 'GET',
    }).catch(err => console.log(err))

    if(res.ok) {
        login(email)
    }
}

async function postSignup(){
    const email = document.getElementById('usernameSignup').value;
    const password = document.getElementById('senhaSignup').value;
    const res = await fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password
        }),
    }).catch(err => console.log(err))

    if(res.ok){
        return console.log(res.status)
    }
}

async function delLogout(){
    const res = await fetch(url + '/auth', {
        method: 'DELETE',
    }).catch(err => console.log(err))

    location.reload();
}

async function getToken(){
    const res = await fetch(url + '/auth/token', {
        method: 'GET',
    }).catch(err => console.log(err))

    if(res.ok) {
        login('')
    }
}

window.onload = getToken();
