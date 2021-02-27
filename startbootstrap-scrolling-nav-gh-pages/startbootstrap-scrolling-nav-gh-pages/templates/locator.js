const locator = '<div>' +
    '<div id="map" class="col-md-12"></div>' +
    '<div class="input-group">' +
        '<div class="input-group-prepend">' +
            '<span class="input-group-text"><img src="../assets/search-24px.svg" onclick="updatelocation()"></span>' +
        '</div>' +
        '<input id="locationinput" type="text" class="form-control" onkeyup="updatelocation()">' +
    '</div>' +
    '<style onload="initialize(new google.maps.LatLng(49.026747, 8.385419))"></style>';