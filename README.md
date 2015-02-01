DepartureTime

Description

My implementation of DepartureTime is a JSON based web service where
one can request departure times from DSB based on a geo-location and a
radius in km.

The service is based on JSON send through HTTP and it can be requested
directly from the browser using three inputs: 
 - latitude
 - longitude
 - radius in km

Requesting all departures from Aarhus within a radius of 10 km would be:

http://89.221.166.70/location=56.1500,10.2167,10


Deployment
- Installing

  You want to change the settings in the wsgi configuration file for
  apache2: install/departuretimes.dk.conf to match the path where the
  project has been checked out and the domain / IP.

  By default the project is checked out in your home folder. 

  To install and setup the DepartureTime project run:

  $ bash install.sh


- Run

  I would suggest to use Screen and then run the following command
  from within Screen:

  $ bash run_services.sh

  Now you should be good to go.
  Try to load the web page.



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

 I have previously worked for about 4 months with Python and Django,
 so I am no expert - and I encounter a few problems on the way,
 i.e. when I wanted to share a dictionary between two threads - but I
 got it working eventually.

 At some point I spend a few weeks playing around with RabbitMQ and I
 decided to try it out some more for this project - which was a lot of
 fun!


Technical choices and architecture

 - Architecture
  
   The system is composed of four main components:
    - a thin web service,
    - a query service,
    - a storage service and
    - a data import service
  
  These services are glued together by RabbitMQ.  I decided to have
  the components coupled together as loosely as possible so each
  component can be switched off without directly affecting the others.
  How ever the resulting solution actually ended up having a quite
  strong coupling of the web service, the query service and the
  storage.  The web service will block until it receives a response
  from the Query service - and the query service will in return block
  until it gets all the data that it needs from the Storage.  The link
  between the Query service and the Storage service could be loosened
  a bit by introducing a cache at the Query service (which would make
  a lot of sense - especially if the end user keeps sending requests
  for almost the same location).
  

 - Trade-offs
   
   The Data store only keeps data in memory and is basically very
   naive.  The paring of geo locations with train stations is not
   satisfying. The geo locations are paired with the train stations
   based on city name and train station names. If a train stop is not
   named by a city, the system will not be able to find a geo location
   for this train station and the train station will not be included
   in the output.
   

 - Left out 

   - Persisting data, 
   - user interface, 
   - proper geo location, 
   - proper automated testing,
   - fully automated deployment,
   - services should be run as daemons or something smarter than
     running inside a screen session.
 

 - What could be done differently
 
   Generally, I think what I have done here is done right but like I
   mentioned above, some of the services might not need to be as
   tightly connected as they are right now.

   I would not change the general architecture, I would add the
   features that are currently missing or change the parts that are
   implemented too naive.

   

Link to other code of pride


Link to resume or public profile


Link to hosted application 
http://89.221.166.70/
