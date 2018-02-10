var map;
// Create a new blank array for all the listing markers.
var markers = [];

var place_loc = {lat: 40.719526, lng: -74.0089934};





// This function populates the infowindow when the marker is clicked. We'll only allow
// one infowindow which will open at the marker that is clicked, and populate based
// on that markers position.
function populateInfoWindow(marker, infowindow) {
    // Check to make sure the infowindow is not already opened on this marker.
    if (infowindow.marker != marker) {
        infowindow.marker = marker;
        infowindow.setContent('<div>' + marker.title + '</div>');
        infowindow.open(map, marker);
        // Make sure the marker property is cleared if the infowindow is closed.
        infowindow.addListener('closeclick',function(){
        infowindow.setMarker = null;
        });
    }
}



function initMap() {
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 40.7413549, lng: -73.9980244},
    zoom: 13
    });
//    var tribeca = {lat: 40.719526, lng: -74.0089934};
    var marker = new google.maps.Marker({
        position: place_loc,
        map: map,
        title: 'First Marker!'
    });
}


function showSelected(){
  var input, filter, table, tr, td, i;
  src = document.getElementById("src-select");
  filter = src.value.toUpperCase();
  table = document.getElementById("news-lst");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}




function getLatLong(url){
    var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    xhr.send();
    };

    getJSON(url,
        function(err, data) {
            if (err !== null) {
            alert('Something went wrong: ' + err);
            } else {
            var pair = document.getElementById("testing").innerHTML = data.results[0].geometry.location;
            place_loc.lat = pair.lat
            place_loc.lng = pair.lng
            }
        }
    );
}

