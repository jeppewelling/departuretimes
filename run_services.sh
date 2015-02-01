
# Restart the rabbit mq to clear up any queues.
sudo service rabbitmq-server restart

# The storage service is responsible for storing data
python -m Storage.run &

# The Query service is responseible for performing calculations on the
# data
python -m Query.run &

# The data import service is responsible for importing data from the
# external data providers, in this case only DSB.
python -m Data.run &


