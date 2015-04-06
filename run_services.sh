# Restart the rabbit mq to clear up any queues.
sudo service rabbitmq-server restart

# The storage service is responsible for storing data
service storage_service start

# The QueryDepartures service is responseible for performing calculations on the
# data
service query_service start

# The data import service is responsible for importing data from the
# external data providers, in this case only DSB.
service data_service start

# Responsible for monitoring the sysetm as it is running
service health_service start




