// document.getElementById("searchInput").addEventListener('input',takeSong);

function displayTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('time').textContent = `Current Time: ${timeString}`;
}
function takeSong(){
    console.log("query")
    let searchQ = document.getElementById("searchInput").value
    const request = new XMLHttpRequest();
    request.onreadystatechange = () => {
    if (request.readyState === 4) {
      giveSong(request.response);
        }
    };
    request.open("GET", "/spotify/search?query="+searchQ);
    request.send("")

}
function giveSong(request){
    console.log(request)
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

// Function to handle form submission for registration
// Registration Helper Function
function registerUser(username, password, password2) {
    // Check if passwords match
    if (password !== password2) {
        alert("Passwords do not match!");
        return;
    }

    // Create the registration data
    let data = {
        username: username,
        password: password,
        password2: password2
    };

    // Make the POST request to register endpoint
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('Registration successful!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    const request = new XMLHttpRequest();
    request.open("GET", "/spotify/login");
    request.setRequestHeader("Content-Type","application/json")
    request.setRequestHeader("Location","/spotify/login")
    request.setRequestHeader("Access-Control-Allow-Origin","*")
    request.send("")


}


//sends out a post request with username and pw info
//auth just needs a function to receive it, if you run the page + go into network you can read the request
function getLogin() {
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    let password2 = null;

    if (document.getElementById("password2").getAttribute("style")=="display: block;") {
         password2 = document.getElementById("password2").value
         registerUser(username, password, password2)
        return;
    }
    const request = new XMLHttpRequest();
    let messageJSON;

    if (password2 != null){
         messageJSON = {"username": username, "password": password, "password2": password2};
    }
    else{
         messageJSON = {"username": username, "password": password};
    }

    request.open("POST", "/login");
    request.setRequestHeader("Content-Type","application/json")

    request.send(JSON.stringify(messageJSON));
}

// set time every second
setInterval(displayTime, 1000);

// Call the location function when the page loads
window.onload = displayLocation;
