
var world_map;

function initMap() {
    world_map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 30.590285, lng: 2.881358},
        zoom: 3
    });

    // add PoP sites to map
    $.get("/api/pops/", function(pops) {
        $.each(pops, function(pop_key, pop_val) {
            var marker = new google.maps.Marker({
                position: pop_val,
                map: world_map,
                title: pop_key
            })
        });
    });

    $.get("/api/feed/stime/1572566400/etime/1574499833/?prefix=128.189.0.0/16"), function(updates_data) {
        console.log(updates_data)
    }

    heatTheMap()
}

function heatTheMap() {
    var heatmapData = [];
    $.get("/api/pop/rv_amsix", function (pop_coords) {
        heatmapData.push(new google.maps.LatLng(pop_coords.lat, pop_coords.lng));
        // .get is async ...
        console.log(heatmapData);
        var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        radius: 15,
        maxIntensity: 1
    });
    heatmap.setMap(world_map);
    });
}

//function popThePoPs(data) {
//}
