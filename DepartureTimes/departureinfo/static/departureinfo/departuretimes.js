(function($){
    
    var Departure = Backbone.Model.extend({
	defaults: {
	    FromStation: "",
	    DestinationName: "",
	    DepartureTime: new Date(),
	    Cancelled: false,
	    Distance: 0,
	    Track: 0
	}
    });

    var List = Backbone.Collection.extend({
	model: Departure,
	render: function () {}
    });




    var ListView = Backbone.View.extend({
	el: $('body'),
	
	events: {
	    'click button#search': 'search'
	},

	initialize: function(){
	    _.bindAll(this, 'render','search', 'renderDepartures');
	    
	    this.collection = new List();
	    this.collection.comparator = 'DepartureTime';


	    this.collection.bind('reset', this.resetDepartures);

	    this.render();
	},

	
	
	render: function(){
	    $(this.el).append(  "<div id=\"ManualControl\">Enter location: lat lon:<br>"
			      + "<input type=\"text\" id=\"Location\" value=\"56.1500 10.2167\"><br>"
			      + "Radius (km):<br>"
			      + "<input type=\"text\" id=\"Radius\" value=\"5\"><br>"
			      + "<button id=\"search\">Search</button><br></div>"
			      +"<div id=\"mapholder\"></div>");
	    
	    $("#ManualControl").hide();
	    
	    var self = this;
	    $(this.el).append("<ul></ul>");
	    _(this.collection.models).each(function(departure){ // in case collection is not empty
		self.renderDeparture(departure);
	    }, this);
	    
	},
	resetDepartures: function() {
	    $('ul', this.el).children().remove();
	},

	renderDepartures: function() {
	    this.resetDepartures();

	    function iconByType(type) {
		if (type == "Train") return "<img src=\"/static/departureinfo/images/train.png\">";
		return "";
	    }

	    // function showPositionInMap(lat, lon) {
	    // 	var latlon = lat + "," + lon;
	    // 	var img_url = "http://maps.googleapis.com/maps/api/staticmap?center="+latlon+"&zoom=14&size=400x300&sensor=false";
	    // 	document.getElementById("mapholder").innerHTML = "<img src='"+img_url+"'>";
	    // }


	    this.collection.forEach(function(departure, i, lst) {
		var departureTime = departure.get('DepartureTime');
		var fromStation = departure.get('FromStation');
		var distance = departure.get('Distance');
		var destinationName = departure.get('DestinationName');
		var type = departure.get('Type');
		$('ul', this.el).append("<li>"
					+""
					+ departureTime 
					+" "
					+ iconByType(type)
					+ fromStation 
					+ " ("+ distance +" km) <span style=\"font-size:25px\">&#8594;</span> "
					+ destinationName
					+"</li>");
	    });
	},

	// void -> void
	search: function() {
	    this.collection.reset();
	    var self = this;
	    
	    // TODO move google maps setup to the render method.
	    function setupGoogleMap(centerLat, centerLon) {
		var lat = centerLat;
		var lon = centerLon;
		var latlon = new google.maps.LatLng(lat, lon);
		var mapholder = document.getElementById('mapholder');
		mapholder.style.height='300px';
		mapholder.style.width='100%';
		
		var myOptions={
		    center:latlon,zoom:14,
		    mapTypeId:google.maps.MapTypeId.ROADMAP,
		    mapTypeControl:false,
		    navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}
		};
		var map = new google.maps.Map(document.getElementById("mapholder"),myOptions);
		return map;
	    }
	    
	    function positionOnMap(lat, lon, map, stationName, destinations)
	    {
		var latlon = new google.maps.LatLng(lat, lon);
		new google.maps.Marker({position:latlon,map:map,title:stationName+"\n"+destinations});
	    }

	    // string -> void
	    function fetchData(url, map) {	
		$.getJSON(url, function(data) {
		    $.each(data, function(key, fromStation) {
			var stationLocation = fromStation.Location;
			var lat = stationLocation.Lat;
			var lon = stationLocation.Lon;
            var departures = fromStation.Departures

            if (departures.length == 0)
                return;


            var departures_description = "";
			$.each(fromStation.Departures, function (i, d) {
			    // Date -> string
			    function formatDate(ms) {
				// int -> string
				function padNumber(n) {
				    if (n < 10) return "0"+n;
				    return n + "";
				}
				
				var date = new Date(ms*1000);
				return padNumber(date.getHours()) +":"+ padNumber(date.getMinutes());
			    }

			    var date = formatDate(d.DepartureTime);
			    var dep = new Departure();
			    dep.set({
				FromStation: fromStation.StationName,
				DestinationName: d.DestinationName,
				DepartureTime: date,
				Cancelled: d.Cancelled,
				Track: d.Track,
				Distance: fromStation.Distance.toFixed(2),
				Type: d.Type
			    });
			    self.collection.add(dep);

			    departures_description += date + " "+ d.DestinationName +"\n"
			});

			positionOnMap(lat, lon, map, fromStation.StationName, departures_description);


		    });
		    self.renderDepartures();
		});
	    }
	    

	    
	    function currentPositionReady(position) {
		var lat = position.coords.latitude;
		var lon = position.coords.longitude;
		var map = setupGoogleMap(lat, lon);

		var radius = $("#Radius").val();
		fetchData(makeUrl(lat, lon, radius), map);
	    }
	    
	    function makeUrl(lat, lon, radius) {
		return "/location="+ lat +","+ lon +","+ radius;
	    }

	    // (error func: void -> a) * (success func: string * map -> a) -> a
	    function getUrlFromTextFiends(error, success) {
		var location = $("#Location").val();
		var coordinates = location.split(/\,\ +| +/);
		if (coordinates.length == 0) return error();
		if (location == "") return error();
		
		var lat = coordinates[0];
		var lon = coordinates[1];
		var map = setupGoogleMap(lat, lon);
		var radius = $("#Radius").val();
		return success(makeUrl(lat, lon, radius), map);
	    }

	    // void -> void
	    // Gets the departures near the current
	    // position. If the position is not available, it shows a
	    // text field where the user can input a geo location
	    // coordinate.
	    function getDepartures() {
		if (navigator.geolocation) {
		    navigator.geolocation.getCurrentPosition(currentPositionReady);
		} else {
		    $("#ManualControl").show();
		    getUrlFromTextFiends(function() {	return ""; }, // on invalid lat, lon, radius data
					 fetchData);
		}
	    }
	    
	    getDepartures();
	}
    });


    var listView = new ListView();
    listView.search();
})(jQuery);			
