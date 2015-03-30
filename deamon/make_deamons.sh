#! /bin/sh

sudo ./make_deamon.sh query_service /srv/departuretimes run_query.py
sudo chmod 755 query_service


sudo ./make_deamon.sh data_service /srv/departuretimes run_data.py
sudo chmod 755 data_service

sudo ./make_deamon.sh storage_service /srv/departuretimes run_storage.py
sudo chmod 755 storage_service

sudo ./make_deamon.sh health_service /srv/departuretimes run_health.py
sudo chmod 755 health_service
