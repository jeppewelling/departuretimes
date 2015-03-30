# Setting up the web project on a fresh Ubuntu machine

echo "Installing Apache..."
sudo apt-get install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

echo "Installing WSGI for Apache..."
sudo apt-get install libapache2-mod-wsgi
sudo service apache2 restart

echo "Installing Django..."
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install Django
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

# Check if directory already exists
sudo mkdir /etc/apache2/sites-available/ 
sudo cp install/departuretimes.dk.conf /etc/apache2/sites-available/departuretimes.dk.conf

# Enabel the virtual host and restart apache
sudo a2ensite departuretimes.dk.conf
sudo service apache2 reload


# Stup the services 
cd deamon
sudo ./make_deamons.sh

sudo mv storage_service /etc/init.d/
sudo chmod 755 /etc/init.d/storage_service
sudo chmod 755 /srv/departuretimes/run_storage.py
sudo update-rc.d storage_service defaults

sudo mv query_service /etc/init.d/
sudo chmod 755 /etc/init.d/query_service
sudo chmod 755 /srv/departuretimes/run_query.py
sudo update-rc.d query_service defaults

sudo mv data_service /etc/init.d/
sudo chmod 755 /etc/init.d/data_service
sudo chmod 755 /srv/departuretimes/run_data.py
sudo update-rc.d data_service defaults

sudo mv health_service /etc/init.d/
sudo chmod 755 /etc/init.d/health_service
sudo chmod 755 /srv/departuretimes/run_health.py
sudo update-rc.d health_service defaults

# Start the departuretime services
# Restart the rabbit mq to clear up any queues.
sudo service rabbitmq-server restart

# The storage service is responsible for storing data
sudo service storage_service start

# The Query service is responseible for performing calculations on the
# data
sudo service query_service start

# The data import service is responsible for importing data from the
# external data providers, in this case only DSB.
sudo service data_service start

# Responsible for monitoring the sysetm as it is running
sudo service health_service start





