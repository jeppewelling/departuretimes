#!/bin/bash

sudo mv storage_service /etc/init.d/storage_service
sudo chmod 755 /etc/init.d/storage_service
sudo chmod 755 /srv/departuretimes/run_query.py
sudo update-rc.d storage_service defaults

sudo mv query_service /etc/init.d/query_service
sudo chmod 755 /etc/init.d/query_service
sudo chmod 755 /srv/departuretimes/run_query.py
sudo update-rc.d query_service defaults

sudo mv data_service /etc/init.d/data_service
sudo chmod 755 /etc/init.d/data_service
sudo chmod 755 /srv/departuretimes/run_data.py
sudo update-rc.d data_service defaults

sudo mv health_service /etc/init.d/health_service
sudo chmod 755 /etc/init.d/health_service
sudo chmod 755 /srv/departuretimes/run_health.py
sudo update-rc.d health_service defaults
