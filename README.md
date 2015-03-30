DepartureTime Take Two

Description

This implementation of DepartureTime is a JSON based web service where
one can request departure times from DSB based on a geo-location and a
radius in km.

The application has a thin Web client that automatically invokes a search
based on the users current location.

The service is based on JSON send through HTTP and it can be requested
directly from the browser using three inputs: 
 - latitude
 - longitude
 - radius in km

Requesting all departures from Aarhus within a radius of 10 km would be:

http://89.221.166.70/location=56.1500,10.2167,10


Deployment
- Installing

 - By default the install script will place the departuretime app in: /srv/departuretimes

      You might want to change the settings in the wsgi configuration file for
      apache2: install/departuretimes.dk.conf to match an alternative path where the
      project has been checked out and the domain / IP.

  - To install and setup the DepartureTime project, download the install.sh file and run:

  $ bash install.sh


- Run

  - After running the install script, the service is available at localhost port 80.
  - The install script starts up the 5 services composing the application
        - Rabbit-server
        - storage_service
        - data_service
        - query_service
        - health_service
   All of these services can be properly stopped, restarted and started by using the service command e.g.:
   $ sudo service data_service start

   For development purpose each service can be started up manually by invoking the run scripts in the project root:
   run_data.py
   run_health.py
   run_query.py
   run_storage.py


Back-end

I jumped into the water in the deep end and started working with
technologies that I have less experience with. My implementation uses
the following technologies:

 - Python
 - Django
 - RabbitMQ
 - Pika (RabbitMQ adapter for Python)
 - Apache2
 - Git
 - Backbone, jQuery, javascript

 I have previously worked for about 4 months with Python and Django,
 so I am no expert - and I encounter a few problems on the way - but I
 got it working eventually.

 At some point I spend a few weeks playing around with RabbitMQ and I
 decided to try it out some more for this project - which was a lot of
 fun!


Technical choices and architecture

 - Architecture

  See diagram.pdf:
  https://github.com/jeppewelling/departuretimes/blob/master/diagram.pdf


  The services depicted in the diagram are glued together with RabbitMQ.
  I decided to have the components coupled together as loosely as possible
  such that each component can be switched off without directly affecting
  the others.  The web service will block until it receives a response
  from the Query service. Making a search from Aarhus with a radius of 5 km
  takes about 1 - 3 ms in the current setup.
  

 - Trade-offs
   
   The Data store only keeps data in memory and its only task is to gather
   data from the data imports and publish this data to the Query services.

   The paring of geo locations with train stations is done through
   Googles georesolver.


 - Left out 

   - Persisting data, 
   - proper automated testing,
   - fully automated deployment,


 - What could be done differently
 

   

Link to other code of pride


Link to resume or public profile


Link to hosted application 

http://89.221.166.70/
