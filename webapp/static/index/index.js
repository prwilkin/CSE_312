function displayTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('time').textContent = `Current Time: ${timeString}`;
}


function displayLocation() {
    // this might use permissions
    navigator.geolocation.getCurrentPosition(function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        document.getElementById('latLong').textContent = `Your Location: Latitude: ${lat}, Longitude: ${lon}`;
    });
}
function displayLogin(formtype) {
    //username label
    const usernameLabel = document.getElementById("UsernameLabel");
    usernameLabel.setAttribute("style","display: block;")

    //username input
    const usernameInput = document.getElementById("username");

    usernameInput.setAttribute("style","display: block;")

    //password label
    const passwordLabel = document.getElementById("PasswordLabel");

    passwordLabel.setAttribute("style","display: block;")
    //password input

    const passwordInput =  document.getElementById("password");

    passwordInput.setAttribute("style","display: block;")
    if (formtype == "registration") {
        //password label
        const confirmLabel = document.getElementById("ConfirmPasswordLabel");

        confirmLabel.setAttribute("style", "display: block;")
        //password input

        const password2Input = document.getElementById("password2");

        password2Input.setAttribute("style", "display: block;")

        //blocking register, displaying login

        const registerButton = document.getElementById("registerButton");
        registerButton.setAttribute("style", "display: none;")
        const loginButton = document.getElementById("loginButton");
        loginButton.setAttribute("style", "display: block;")
    } else{
         //password confirmation label
        const confirmLabel = document.getElementById("ConfirmPasswordLabel");
        confirmLabel.setAttribute("style","display: none;")
        //password confirmation

        const password2Input =  document.getElementById("password2");
        password2Input.setAttribute("style","display: none;")
        //blocking login, displaying register
        const registerButton = document.getElementById("registerButton");
        registerButton.setAttribute("style", "display: block;")
        const loginButton = document.getElementById("loginButton");
        loginButton.setAttribute("style", "display: none;")
    }
    //submit button
        const submitButton = document.getElementById("SubmitButton");
        submitButton.setAttribute("style", "display: block;")


}

//sends out a post request with username and pw info
//auth just needs a function to receive it, if you run the page + go into network you can read the request
function getLogin() {
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    let password2 = null;
    if (document.getElementById("password2").getAttribute("style")=="display: block;") {
         password2 = document.getElementById("password2").value
    }

    const request = new XMLHttpRequest();
    let messageJSON;

    if (password2 != null){
         messageJSON = {"username": username, "password": password, "password2": password2};
    }
    else{
         messageJSON = {"username": username, "password": password};
    }
    request.open("POST", "/");
    request.send(JSON.stringify(messageJSON));
}

// set time every second
setInterval(displayTime, 1000);

// Call the location function when the page loads
window.onload = displayLocation;
