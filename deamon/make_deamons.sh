#! /bin/sh

./make_deamon.sh query_service /srv/departuretimes run_query.py 
chmod 755 query_service


./make_deamon.sh data_service /srv/departuretimes run_data.py
chmod 755 data_service

./make_deamon.sh storage_service /srv/departuretimes run_storage.py
chmod 755 storage_service
