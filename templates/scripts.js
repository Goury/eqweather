function getAjax (url, callback, fallback) {
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4) {
			if (xmlhttp.status == 200) {
				callback(xmlhttp.responseText);
			} else {
				fallback(xmlhttp.responseText);
			}
		}
	}
	xmlhttp.open('GET', url, true);
	xmlhttp.send();
}

function doNothing(){}

window.addEventListener("map:init", function (e) {
	var detail = e.detail;
	var legend = L.control({position: 'bottomright'});
	legend.onAdd = function (map) {
		var div = L.DomUtil.create('div', 'info legend');
		div.innerHTML += '<i style="background: red"></i>more humid and more hot<br>';
		div.innerHTML += '<i style="background: purple"></i>more humid but less hot<br>';
		div.innerHTML += '<i style="background: orange"></i>less humid but more hot<br>';
		div.innerHTML += '<i style="background: green"></i>less humid and less hot<br>';
		div.innerHTML += '<i style="background: yellow"></i>No data loaded<br>';
		return div;
	};
	legend.addTo(detail.map);
	window.map = detail.map;
}, false);



window.cells = [];
window.polygons = {};
window.buttons = [];

function drawPolygons(cells){
	var points;
	var min_x = 180;
	var max_x = -180;
	var min_y = 180;
	var max_y = -180;
	for (i=0; i<cells.length; i++) {
		if (cells[i].polygon_json) {
			cell_id = cells[i].id;
			points = JSON.parse(cells[i].polygon_json);
			window.polygons[cell_id] = L.polygon(points, {color: 'yellow'});
			window.polygons[cell_id].bindTooltip(cell_id+'<br>'+cells[i].grid_id+'<br>X: '+cells[i].grid_x+'<br>Y:'+cells[i].grid_y)
			window.polygons[cell_id].addTo(window.map);
			for (j=0; j<points.length; j++) {
				min_x = Math.min(min_x, points[j][0]);
				max_x = Math.max(max_x, points[j][0]);
				min_y = Math.min(min_y, points[j][1]);
				max_y = Math.max(max_y, points[j][1]);
			}
		}
	}
	window.map.fitBounds(L.polygon([[min_x, min_y], [max_x, max_y]]).getBounds());
}

function CellLoader(callback){
	var data = JSON.parse(callback);
	window.cells = window.cells.concat(data.results);
	if (data.next) {
		getAjax(data.next, CellLoader, doNothing);
	} else {
		drawPolygons(window.cells);
	}
}

getAjax('{% url "api:cells" %}', CellLoader, doNothing);

function recolorPolygons(forecasts){
	var total_temp = 0;
	var total_humid = 0;
	for (i=0; i<forecasts.length; i++) {
		total_temp += parseFloat(forecasts[i].temperature);
		total_humid += parseFloat(forecasts[i].humidity);
	}
	for (i=0; i<forecasts.length; i++) {
		var poly = window.polygons[forecasts[i].cell_id];
		var more_humid = parseFloat(forecasts[i].humidity) > total_humid/forecasts.length
		var more_hot = parseFloat(forecasts[i].temperature) > total_temp/forecasts.length

		if (more_humid) {
			if (more_hot) {
				poly.setStyle({color: 'red', fillColor:'red'});
			} else {
				poly.setStyle({color: 'purple', fillColor:'purple'});
			}
		} else {
			if (more_hot) {
				poly.setStyle({color: 'orange', fillColor:'orange'});
			} else {
				poly.setStyle({color: 'green', fillColor:'green'});
			}
		}
	}
}

function drawForecast(callback){
	var data = JSON.parse(callback);
	window.forecasts = window.forecasts.concat(data.results);
	if (data.next) {
		getAjax(data.next, drawForecast, doNothing);
	} else {
		recolorPolygons(window.forecasts);
	}
}

function renderButtons(buttons){
	for (i=0; i<buttons.length; i++) {
		button = document.createElement('button');
		button.innerHTML = buttons[i].human_readable_when;
		button.setAttribute('onclick', 'window.forecasts = []; getAjax("'+buttons[i].when+'", drawForecast, doNothing);');
		document.getElementById('buttons').appendChild(button);
	}
}

function TimeButtons(callback){
	var data = JSON.parse(callback);
	window.buttons = window.buttons.concat(data.results);
	if (data.next) {
		getAjax(data.next, TimeButtons, doNothing);
	} else {
		renderButtons(window.buttons);
	}
}

getAjax('{% url "api:times" %}', TimeButtons, doNothing);
