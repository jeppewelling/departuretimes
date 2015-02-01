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
cd ~
git clone https://github.com/jeppewelling/departuretimes.git

# I was unable to make this work. Eventually I just used Emacs to make
# the file and inserted the text below.
sudo cp install/departuretimes.dk.conf /etc/apache2/sites-available/departuretimes.dk.conf

# Enabel the virtual host and restart apache
sudo a2ensite departuretimes.dk
sudo /etc/init.d/apache2 reload
