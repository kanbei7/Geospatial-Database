var map;

// 畫熱圖
function draw_heatmap(results) {
  var heatmapData = [];

  for (var i = 0; i < results.points.length; i++) {

    // 取得座標
    var coords = results.points[i].coord;

    // 要注意： LatLng 物件的經緯度順序與 GeoJSON 的座標順序相反
    var latLng = new google.maps.LatLng(coord[1], coord[0]);

    var weightedLoc = {
      // 位置
      location: latLng,
      // 單位強度
      weight: results.points[i].weight
    };

    heatmapData.push(weightedLoc);
  }

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData,
    dissipating: true,
    map: map,
    radius: 40,
    gradient: ['transparent', '#00f', '#0f0', '#f00']
  });
}


function initialize() {
  var mapElement = document.getElementById("mapDiv");

  map = new google.maps.Map(mapElement, { 
    center: new google.maps.LatLng(47.6219, -122.3197),
    zoom: 15,
    mapTypeId: 'satellite'
  });
  
  $.ajax({
    type: 'get',
    url: 'test.json',
    success: function(data){
      // 將取得的資料轉為 json
      var geoJson = JSON.parse(data);
      // 畫熱圖
      draw_heatmap(geoJson);
    }
  });
  
  
}





 function loadFile() {
    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
      alert("The file API isn't supported on this browser yet.");
      return;
    }

    input = document.getElementById('fileinput');
    if (!input) {
      alert("Um, couldn't find the fileinput element.");
    }
    else if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
      alert("Please select a file before clicking 'Load'");
    }
    else {
      file = input.files[0];
      fr = new FileReader();
      fr.onload = receivedText;
      fr.readAsText(file);
    }

    function receivedText(e) {
      lines = e.target.result;
      var newArr = JSON.parse(lines); 
    }
  }