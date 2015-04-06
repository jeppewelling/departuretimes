DepartureTime Take Two

Description

This implementation of DepartureTime is a JSON based web service providing departure times from DSBs web feed.
Departures can be requested by geo-location and radius.

The application has a thin Web client that automatically invokes a search
based on the users current location.

The service is based on JSON send through HTTP and it can be requested
directly from the browser using three inputs: 
 - latitude
 - longitude
 - radius in km

Requesting all departures from Aarhus within a radius of 10 km would be:

http://89.221.166.70/location/56.1500,10.2167,10


- Installing

   The install script will place the departuretime app in: /srv/departuretimes
   The default domain name is set to be departuretimes.dk, thus make a mapping in the hosts file from 127.0.0.1 to
   departuretimes.dk and it should be possible to access the webservice locally.
   Alternatively change the wsgi settings file located in /etc/apache2/sites-available/departuretimes.dk.conf

  - To install and setup the DepartureTime project, download the install.sh file and run:

  $ wget https://raw.githubusercontent.com/jeppewelling/departuretimes/master/install.sh
  $ bash install.sh


- Run

  - After running the install script, the service is available at departuretimes.dk (localhost) port 80.
  - The install script starts up the 5 services composing the application
        - Rabbit-server
        - storage_service
        - data_service
        - query_service
        - health_service
   All of these services can be stopped, restarted and started by using the service command e.g.:
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

 I have previously worked with Python and Django for about 4 months,
 so I am no expert - and I did encounter a few problems on the way - but I
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
  the others.
  The Query service is continuously updated with the latest state from the
  storage by subscribing to the storage's publish queue.  There could be any
  number of active query services to facilitate searching. Load balancing
  across the query services is handled by Rabbit MQ in a round robin fashion.
  The web service will block until it receives a response from the Query service.
  The typical response time for a search from Aarhus H with a radius of 5 km is
  between 30 and 50 ms, where the majority of the time is network overhead from Apache2.
  Making the same search outside of Apache context takes about 5 ms (interesting).


 - Trade-offs
   
   The Data store only keeps data in memory and its only task is to gather
   data from the data imports and publish this data to the Query services.

   The paring of geo locations with train stations is done through
   Googles georesolver.


 - Left out 
   - Persisting data,
   - proper automated testing,


 - What could be done differently
 

   

Link to other code of pride


Link to resume or public profile


Link to hosted application 

http://89.221.166.70/
