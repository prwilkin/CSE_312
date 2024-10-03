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

// set time every second
setInterval(displayTime, 1000);

// Call the location function when the page loads
window.onload = displayLocation;
