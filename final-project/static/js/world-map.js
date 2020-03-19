var torontoNeighbourHoodsBoundaries  = "https://opendata.arcgis.com/datasets/af500b5abb7240399853b35a2362d0c0_0.geojson";
var heatmapLayer="http://127.0.0.1:5000/api/heatmap"

var naighbourhoods = new L.LayerGroup();

d3.json(torontoNeighbourHoodsBoundaries, function (geoJson) {
  L.geoJSON(geoJson.features, {
      onEachFeature: function (feature, layer) {
        layer.bindPopup(layer.feature.properties.Neighbourhood);
      }
  }).addTo(naighbourhoods);
  createMap(naighbourhoods);
});

var heatmap = new L.LayerGroup();

d3.json(heatmapLayer, function(data) {
    var heatArray = [];

    for (var i = 0; i < data.length; i++) {
      var location = data[i].coordinates;
      if (location) {
        heatArray.push([location[0], location[1]]);
      }
    }
    var heat = L.heatLayer(heatArray, {
      radius: 20,
      blur: 35
    }).addTo(heatmap);    
}); 

function createMap(){
  var satellite = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>',
    maxZoom: 13,
    id: 'mapbox.satellite',
    accessToken: API_KEY
  });
  var grayscale = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>',
      maxZoom: 13,
      id: 'mapbox.light',
      accessToken: API_KEY
  });

  var outdoors = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>',
      maxZoom: 13,
      id: 'mapbox.outdoors',
      accessToken: API_KEY
  });
  var dark = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>',
      maxZoom: 13,
      id: 'mapbox.dark',
      accessToken: API_KEY
  });
  
  var baseLayers = {
      "Satellite": satellite,
      "Grayscale": grayscale,
      "Outdoors": outdoors,
      "Dark": dark
  };

  var overlays = {
    "Neighbourhoods": naighbourhoods,
    "Crime Heatmap": heatmap,
  };  
  
  var myMap = L.map("map", {
    center: [43.6532, -79.3832],
    zoom: 10,
    layers: [satellite, naighbourhoods, heatmap]
  });

  L.control.layers(baseLayers, overlays).addTo(myMap);
}