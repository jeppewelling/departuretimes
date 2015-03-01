# Setting up the web project on a fresh Ubuntu machine

echo "Installing Apache..."
sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

echo "Installing WSGI for Apache..."
sudo apt-get install libapache2-mod-wsgi
sudo service apache2 restart

echo "Installing Django..."
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
sudo pip install Djang
sudo pip install pika



echo "Installing RabbitMQ..."
sudo apt-get install rabbitmq-server


# Setup web application
sudo apt-get install git

# Add the user who should execute the services
sudo useradd departuretimes_user


cd /srv
sudo git clone https://github.com/jeppewelling/departuretimes.git
sudo chmod 755 -R departuretimes/DepartureTimes
cd departuretimes


sudo mkdir /etc/apache2/sites-available/ 
sudo cp install/departuretimes.dk.conf /etc/apache2/sites-available/departuretimes.dk.conf

# Enabel the virtual host and restart apache
sudo a2ensite departuretimes.dk.conf
sudo service apache2 reload


# Stup the services 
sudo cp Storage/etc/init.d/storage_service /etc/init.d/storage_service
sudo chmod 755 /etc/init.d/storage_service
sudo chmod 755 /srv/departuretimes/start_storage.sh
sudo update-rc.d storage_service defaults

sudo cp Query/etc/init.d/query_service /etc/init.d/query_service
sudo chmod 755 /etc/init.d/query_service
sudo chmod 755 /srv/departuretimes/start_query.sh
sudo update-rc.d query_service defaults

sudo cp Data/etc/init.d/data_service /etc/init.d/data_service
sudo chmod 755 /etc/init.d/data_service
sudo chmod 755 /srv/departuretimes/start_data.sh
sudo update-rc.d data_service defaults


# Start the departuretime services
# TODO ... 
