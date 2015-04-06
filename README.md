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

  - To install and setup the DepartureTime project, execute the two commands:

  $ wget https://raw.githubusercontent.com/jeppewelling/departuretimes/master/install.sh
  $ sudo bash install.sh


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

   After installing the system, it takes about 5 to 10 minutes before the initial data has been imported from DSB.


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

  - The health service
        is responsible for logging information about the system health,
        currently it only tracks the time it takes for a search to pass through the web-application
        and be returned to the end user.
        The health service contains a PID algorithm that determines if additional query-service workers
        should be spawned to help consume search requests.

  - The Query service
        is responseible for carrying out the actual searches in the data received from the store.

  - The Data store service
        is responsible for keeping track of all incoming data from the data providers.
        It broadcasts the data to the query service(s) that has subscribed to the storage services data feed.

  - The Data service
        is responsible for importing data from the data providers and adding geo-locations to these data.
        It ensures that the data are requested in a fair way, avoiding DoS.


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
   At first it might seem a bit naive, but on the other hand, the nature of
   the system is to continuously request data, so data never get old and we
   are not interested in old data any way.


 - Left out 
   - Persisting data,
   - proper automated testing,
   - Administration module for monitoring the system,
   - Logging of exceptions,
   - Logging of system relevant informations - i.e. did some service break down?
   - No plan B for messaging, if RabbitMQ breakes down all fails,
   - No load balancing for the web application,
   - Additional traffic feeds (Rejsepnanen's feed),

 - What could be done differently
    Internally I represent data purely as dictionaries which has a close resemblance with the JSON format,
    but I should probably have modelled this as a class with a "convertToJson" method.

   

Link to hosted application

http://89.221.166.70/
