var map = new L.Map('leaflet', {
	layers: [
		new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			'attribution': 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
		})
	],
	center: [38.727897, -9.164737],
	zoom: 13
});


var sidebar = L.control.sidebar('sidebar', {
		position: 'left'
});

map.addControl(sidebar);

var marker = L.marker([0,0]).addTo(map).on('click', function(){
	sidebar.setContent('Null Island').show();
});


var marker2 = L.marker([40,40]).addTo(map).on('click', function(){
	sidebar.setContent('Somewhere else').show();
});

