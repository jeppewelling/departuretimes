var model = null;

$(document).ready(function() {
(function($){
    // Date -> string
    function formatDate(ms) {
        // int -> string
        function padNumber(n) {
            if (n < 10) return "0"+n;
            return n + "";
        }

        var date = new Date(ms*1000);
        return padNumber(date.getUTCHours()) +":"+ padNumber(date.getUTCMinutes());
    }

    // Models
    var Place = Backbone.Model.extend({
        defaults: {
            Place:"",
            Location: {Lat: 0, Lon: 0}
        }
    });

    var PlaceList = Backbone.Collection.extend({
        url: "/places",
        model: Place,
        comparator: 'Place'
    });

    var PlaceView = Backbone.View.extend({
        tagName: "select",

        append: function(place) {
            var location = place.get('Location').Location
            var lat = location.Lat
            var lon = location.Lon
            key = lat +","+lon
            var value = place.get('Place')
            this.$el.append($('<option>', { value : key }).text(value));
        },

        events: {
            'change' : 'placeSelected'
        },

        placeSelected: function() {
            var location = this.$el.val();
            var coordinates = location.split(/,/);
            var lat = parseFloat(coordinates[0]);
            var lon = parseFloat(coordinates[1]);
            model.moveToPosition(lat, lon);
        },

        initialize: function() {
            this.listenTo(this.model, 'sync', this.render);
        },

        render: function() {
            this.$el.children().remove();
            this.$el.append($('<option>', { value : '0' }).text("Jump to place"));
            var model = this.model;
            model.each(this.append, this);
            $("#places").append(this.$el);
            return this;
        },
    });


    // A departure
    var Departure = Backbone.Model.extend({
        defaults: {
            DestinationName: "Its a blank!",
            DepartureTime: 0,
            Cancelled: false,
            Type: "",
        }
    });

    var DepartureList = Backbone.Collection.extend({
        model: Departure,
        comparator: 'DepartureTime'
    });

    // A location with n departures
    var DepartureLocation = Backbone.Model.extend({
        defaults: {
            StationName: "Im blank",
            Distance: 0,
            Location: {Lat: 0, Lon: 0},
            Departures: new DepartureList()
        },
    })

    var DepartureLocationList = Backbone.Collection.extend({
       // url: '/location/56.1500,10.2167,10',
        model: DepartureLocation,
        comparator: 'Distance',


    });




    // The departureTimes data model containing the current state
    var DepartureTimes = Backbone.Model.extend({
        urlRoot: '/location',

        defaults: {
                Position: null,
                Radius: 5, // km
                DepartureLocations: new DepartureLocationList(),
        },

        initialize: function() {
            this.getUserPosition();
            this.startTimer();
        },

        startTimer: function() {
            var updateIntervalInMs = 5 * 60 * 1000 // 5 minutes
            var self = this;
            setInterval(function() {
                self.getUserPosition();
            }, updateIntervalInMs);
        },

        // Called when fetch has retrieved the new departure times,
        // Parse the JSON input to the model.
        parse: function(departureLocationsJson) {
            var list = this.get('DepartureLocations');
            list.reset();

            function parseDepartures(departures) {
                var list = new DepartureList();
                list.add(_.map(departures, function (d) {
                    return new Departure({DestinationName: d.DestinationName,
                                          DepartureTime: d.DepartureTime,
                                          Cancelled: d.Cancelled,
                                          Type: d.Type});
                }));
                return list;
            }

            list.add(_.map(departureLocationsJson, function(d) {
                return new DepartureLocation({StationName: d.StationName,
                                        Distance: d.Distance,
                                        Location: d.Location,
                                        Departures:parseDepartures(d.Departures)});
            }));

            // Basically this is ignored...
            return departureLocationsJson;
        },

        search: function (lat, lon, radius) {
            var options = {url: this.urlRoot + "/" + lat +","+ lon +","+ radius};
            return Backbone.Model.prototype.fetch.call(this, options);
        },

        moveToPosition: function (lat, lon) {
            this.set('Position', {Lat: lat, Lon: lon});
            this.search(lat, lon, this.get('Radius'));
        },


        onUserPositionFound: function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            this.set('Position', {Lat: lat, Lon: lon});
            this.search(lat, lon, this.get('Radius'));
        },

        onUserPositionNotFound: function() {
        },

        getUserPosition: function() {
            var self = this;
            navigator.geolocation.getCurrentPosition(
                function (position) { self.onUserPositionFound(position); },
                function () { self.onUserPositionNotFound(); });
        }
    });


    // Views

    // The complete application put together.
    var DepartureTimesApplication = Backbone.View.extend({
        el: $("#departureTimesApplication"),

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },

        render: function() {

            var departureLocations = this.model.get('DepartureLocations');
            var listView = new DepartureLocationListView({model: departureLocations});
            var mapView = new DepartureTimesGoogleMapsView({model: this.model});

            // Reset the containers
            this.$("#departureLocationsMap").children().remove();
            this.$("#departureLocationsList").children().remove();

            this.$("#departureLocationsMap").append(mapView.render().el);
            this.$("#departureLocationsList").append(listView.render().el);
        }

    });


    // A view for a single DepartureLocations
    var DepartureLocationView = Backbone.View.extend({
        tagName:  "div",

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },

        template: _.template($('#departure-location-template').html()),

        render: function() {

            // The Json for the template
            function asJson(departureLocation, departure) {
                function typeToIcon(type) {
                    if (type == "Train") return "train.png";
                    return "";
                }

                var icon = typeToIcon(departure.get('Type'));
                var stationName = departureLocation.get('StationName');
                var distance = departureLocation.get('Distance').toFixed(2);
                var destinationName = departure.get('DestinationName');
                var departureTime = formatDate(departure.get('DepartureTime'));

                return {Icon: icon,
                        StationName: stationName,
                        Distance: distance,
                        DestinationName: destinationName,
                        DepartureTime: departureTime};
            }


          var self = this;
          var departures = this.model.get('Departures');
          departures.each(function(v) {
                self.$el.append(self.template(asJson(self.model, v)));
          });

          return this;
        },
    });


    // A view for a list of DepartureLocations
    var DepartureLocationListView = Backbone.View.extend({
        tagName: "div",

        append: function(departureLocation) {
            var view = new DepartureLocationView({model: departureLocation});
            this.$el.append(view.render().el);
        },

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },

        render: function() {
            this.$el.children().remove();
            var departureLocations = this.model;
            departureLocations.each(this.append, this);
            return this;
        },


    });


    // Google maps view
    // This is a view that requires the entire departureTimes data model.
    var DepartureTimesGoogleMapsView = Backbone.View.extend({
        tagName: "div",

        initialize: function() {
            this.map = null;
            // Listen to when the users position is loaded or changed
            this.listenTo(this.model, 'change:Position', this.onPositionChange);
            this.listenTo(this.model, 'change:DepartureLocations', this.onDepartureLocationsChange);
       },

        onDepartureLocationsChange: function() {
            console.log("MapsView.onDepartureLocationsChange");
        },

        onPositionChange: function() {
            var position = this.model.get('Position');
            if (position == null) return;

            var departureLocations = this.model.get('DepartureLocations');
            this.initializeMap(position.Lat, position.Lon);
            this.plotDepartureLocationsOnMap(departureLocations);
        },




        initializeMap: function(lat, lon) {
            var latLon = new google.maps.LatLng(lat, lon);
            var mapContainer = document.getElementById('departureLocationsMap');
            mapContainer.style.height='300px';
            mapContainer.style.width='100%';

            var myOptions={
                center:latLon,zoom:14,
                mapTypeId:google.maps.MapTypeId.ROADMAP,
                mapTypeControl:false,
                navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}
            };
            this.map = new google.maps.Map(mapContainer,myOptions);
        },

        plotDepartureLocationsOnMap: function(departureLocations) {
            var self = this;
            departureLocations.each(function (departureLocation) {
                self.plotDepartureLocationOnMap(departureLocation);
            });
        },

        plotDepartureLocationOnMap: function(departureLocation) {
            if (this.map == null) return;
            var departures = departureLocation.get('Departures');

            // Only plot a location on the map if there are departures from the locaion.
            if (departures.size() == 0) return;

            function prettyPrintDepartures(name, departures) {
                return "<b>" + name + "</b><br>"
                + departures.map(function(d) {
                    return formatDate(d.get('DepartureTime')) +" "+ d.get('DestinationName');
                }).join("<br>");
            }


            var location = departureLocation.get('Location')
            var name = departureLocation.get('StationName');
            var lat = location.Lat;
            var lon = location.Lon;
            var latlon = new google.maps.LatLng(lat, lon);

            var marker = new google.maps.Marker({position:latlon,map:this.map,title:name});


            var map = this.map;
            google.maps.event.addListener(marker, 'click', function() {
                var coordInfoWindow = new google.maps.InfoWindow();
                coordInfoWindow.setContent(prettyPrintDepartures(name, departures));
                coordInfoWindow.setPosition(latlon);
                coordInfoWindow.open(map);
            });
        },

        render: function() {
            this.$el.children().remove();
            this.onPositionChange();
            return this
        }
    });


    model = new DepartureTimes({
                Position: {lat: 0, lon: 0},
                Radius: 5, // km
                });

    var app = new DepartureTimesApplication({model: model});

    var p = new PlaceList();
    p.fetch();
    var pp = new PlaceView({model: p, departureTimesModel: model});

})(jQuery)});