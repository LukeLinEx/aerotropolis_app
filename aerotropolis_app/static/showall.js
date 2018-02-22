var map;
// Create a new blank array for all the listing markers.
var markers = [];
function initMap() {
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7413549, lng: -73.9980244},
        zoom: 13
    });
    // These are the real estate listings that will be shown to the user.
    // Normally we'd have these in a database instead.
//    var locations = [
//            {title: 'Park Ave Penthouse', location: {lat: 40.7713024, lng: -73.9632393}},
//            {title: 'Chelsea Loft', location: {lat: 40.7444883, lng: -73.9949465}},
//            {title: 'Union Square Open Floor Plan', location: {lat: 40.7347062, lng: -73.9895759}},
//            {title: 'East Village Hip Studio', location: {lat: 40.7281777, lng: -73.984377}},
//            {title: 'TriBeCa Artsy Bachelor Pad', location: {lat: 40.7195264, lng: -74.0089934}},
//            {title: 'Chinatown Homey Space', location: {lat: 40.7180628, lng: -73.9961237}}
//    ];

    var locations = kwords;
    console.log(kwords)



    var largeInfowindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();
    // The following group uses the location array to create an array of markers on initialize.
    for (var i = 0; i < locations.length; i++) {
        // Get the position from the location array.
        var position = locations[i].location;
        var title = locations[i].title;
        // Create a marker per location, and put into markers array.
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            id: i
        });
        // Push the marker to our array of markers.
        markers.push(marker);
        // Create an onclick event to open an infowindow at each marker.
        marker.addListener('click', function() {
        populateInfoWindow(this, largeInfowindow);
        });
        bounds.extend(markers[i].position);
    }
    // Extend the boundaries of the map for each marker
    map.fitBounds(bounds);
    }