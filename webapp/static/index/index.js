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
//sends out a post request with username and pw info
//auth just needs a function to recieve it, if you run the page + go into network you can read the request
function getLogin(){
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    const request = new XMLHttpRequest();
    let messageJSON = {"username": username,"password":password};
    request.open("POST", "/");
    request.send(JSON.stringify(messageJSON));
}

// set time every second
setInterval(displayTime, 1000);

// Call the location function when the page loads
window.onload = displayLocation;
