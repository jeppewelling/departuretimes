#!/bin/bash

sudo mv storage_service /etc/init.d/storage_service
sudo chmod 755 /etc/init.d/storage_service
sudo chmod 755 /srv/departuretimes/start_storage.sh
sudo update-rc.d storage_service defaults

sudo mv query_service /etc/init.d/query_service
sudo chmod 755 /etc/init.d/query_service
sudo chmod 755 /srv/departuretimes/start_query.sh
sudo update-rc.d query_service defaults

sudo mv data_service /etc/init.d/data_service
sudo chmod 755 /etc/init.d/data_service
sudo chmod 755 /srv/departuretimes/start_data.sh
sudo update-rc.d data_service defaults
