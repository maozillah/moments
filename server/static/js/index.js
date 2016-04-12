var prox = false;
var fenceX = 43.470151;
var fenceY = -79.701940; //hardcoded
var pos = {
    lat: 0,
    lng: 0
};
var igLocIdData, igLocPhotos;

// determine current location / watch for changes
if (navigator.geolocation) {
    navigator.geolocation.watchPosition(showPosition); //position changes
}

function loadMap() {
    if (!(pos.lat == 0 && pos.lng == 0)) {
        initMap(pos.lat, pos.lng);
    } else {
        setTimeout(function() {
            loadMap();
        }, 1000);
    }
}

function showPosition(position) {
    pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
}

function initMap(latitude, longitude) {
    var myLatlng = {
        lat: latitude,
        lng: longitude
    };

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: myLatlng,
        disableDefaultUI: true
    });

    // marker
    map.addListener('click', function(event) {
        var clickPos = {
            lat: event.latLng.lat(),
            lng: event.latLng.lng()
        }

        submitCurrentLoc(clickPos);

        var marker = new google.maps.Marker({
            position: clickPos,
            map: map
        });

        marker.addListener('click', function(event) {
            marker.setMap(null);
        });
    });
}

function submitCurrentLoc(clickPos) { 
    var coordinates = clickPos.lat + "," + clickPos.lng;

    $.ajax({
        url: "/moment",
        dataType: 'json',
        type: 'POST',
        data: coordinates,
        success: function(data) {
          console.log(data);
        }.bind(this),
        error: function(xhr, status, err) {
          console.error("posting to server", status, err.toString());
        }.bind(this)
      });
}

// initiate google maps
loadMap();