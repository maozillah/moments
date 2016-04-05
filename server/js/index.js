var prox = false;
var fenceX = 43.470151;
var fenceY = -79.701940; //hardcoded
var stop = false;
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

    if (Math.sqrt(Math.pow(fenceX - position.coords.latitude, 2) + Math.pow(fenceY - position.coords.longitude, 2)) <= 0.001) {
        prox = true;
        // bluetoothSerial.write("a");
    } else {
        prox = false;
        // bluetoothSerial.write("b");
    }
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

        igLocSearch(clickPos);

        var marker = new google.maps.Marker({
            position: clickPos,
            map: map
        });

        marker.addListener('click', function(event) {
            marker.setMap(null);
        });
    });
}


// server side code

function igLocSearch(clickPos) {
    var igApi = "https://api.instagram.com/v1/locations/search?access_token=" + igKey;
    var igLat = "&lat=" + clickPos.lat;
    var igLng = "&lng=" + clickPos.lng;

    //TODO: get all location ids?
    $.ajax({
        url:  igApi + igLat + igLng,
        dataType: 'jsonp',
        cache: false,
        success: function(data) {
           igLocIdData = data.data;
            console.log(igLocIdData);
            getLocPhotos(igLocIdData);
        }.bind(this),
        error: function(xhr, status, err) {
            console.error("retrieving location id", status, err.toString());
        }.bind(this)
    });
}


function getLocPhotos(locData) {
    // get media
    //TODO: better way than just getting the first location id, if no images exist, try next location id
    var igLocApi = "https://api.instagram.com/v1/locations/";
    var locId = locData[0].id + "/media/recent?access_token=" + igKey; 

    $.ajax({
        url:  igLocApi + locId,
        dataType: 'jsonp',
        cache: false,
        success: function(data) {
            igLocPhotos = data.data;
            console.log(data);
            console.log(igLocPhotos);

            $( "#images" ).empty();

            for (i = 0; i < igLocPhotos.length; i++) { 
                $( "#images" ).append( "<img src=\"" + igLocPhotos[i].images.thumbnail.url+"\">" + "<p>"+igLocPhotos[i].caption.text+"<p/>" + "<p>"+igLocPhotos[i].location.latitude+igLocPhotos[i].location.longitude+"<p/>");

                // console.log(igLocPhotos[i].images.thumbnail.url);
                //  console.log(igLocPhotos[i].caption.text);
            }

        }.bind(this),
        error: function(xhr, status, err) {
            console.error("retrieving location id", status, err.toString());
        }.bind(this)
    });
}

// initiate google maps
loadMap();