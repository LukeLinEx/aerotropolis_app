var tmp_lst=[];

function initAutocomplete() {
    var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 25.0083024, lng: 121.3028680},
        zoom: 11.3,
        mapTypeId: 'roadmap'
    });

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);

    //map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });

//    google.maps.event.addListener(map, 'click', function( event ){
//        console.log( "Latitude: "+event.latLng.lat()+" "+", longitude: "+event.latLng.lng() );
//    });

    google.maps.event.addListener(map, 'click', function( event ){
        getInfoFromMap(event.latLng.lat(), event.latLng.lng());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function(marker) {
            marker.setMap(null);
        });
        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }

            var infowindow = new google.maps.InfoWindow();
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            var marker = new google.maps.Marker({
                map: map,
                icon: icon,
                title: place.name,
                position: place.geometry.location
            })

            markers.push(marker);

            // Testing area!!
            (function(marker, place){
                marker.addListener('click', function() {




                getInfoFromMap(
                    lat=marker.position.lat(), lng=marker.position.lng(),
                    keyword=place.name, formatted_address=place.formatted_address
                    )





                var content = "<h1>"+place.name+"</h1>";
                content += "<p>"+place.formatted_address+"</p>";
                if (place.formatted_phone_number) {
                content += "<p>Phone:&nbsp;"+place.formatted_phone_number+"</p>";
                }
                infowindow.setContent(content);
                infowindow.open(map, marker);
                });
            })(marker, place);

            // Testing area ends!


            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
        });

}


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



function getInfoFromMap(lat, lng, keyword="", formatted_address=""){
    var form = document.getElementById("form");
    form.getElementsByTagName("input").kword.value = keyword;
    form.getElementsByTagName("input").lat.value = lat;
    form.getElementsByTagName("input").lng.value = lng;
    form.getElementsByTagName("input").address.value=formatted_address;
}

function formToTmpLst(tag){
    var form = tag.parentElement;
    var keyword = form.getElementsByTagName("input").kword.value;

    //stop if keyword is empty
    if(keyword==""){return;}

    var lat = form.getElementsByTagName("input").lat.value;
    var lng = form.getElementsByTagName("input").lng.value;
    var address = form.getElementsByTagName("input").address.value;
    var doc = {
        keyword: keyword, location: {lat: lat, lng:lng}, address:address
    }


    var existing = false;
    for(var i=0; i<kwords.length; i++){
        if(keyword == kwords[i].keyword){
            existing=true;
            var r = confirm("關鍵字已存在，確定變更？");
            if (r == true) {
                tmp_lst.push(doc);
                add_tmp_lst_keyword(keyword);
            }
            break;
        }
    }
    if(!existing){
        tmp_lst.push(doc);
        add_tmp_lst_keyword(keyword);
    }
}


function add_tmp_lst_keyword(keyword){
    var node = document.createElement("li");
    node.innerHTML = keyword;
    document.getElementById("kword2insert").appendChild(node);
}





function godb(){
    var xhttp = new XMLHttpRequest();
    url="?doc=" + JSON.stringify(tmp_lst);
    xhttp.open("POST", url, true);
    xhttp.send();
    location.reload();
}


