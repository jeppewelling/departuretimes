import pika

# A generic send-to-queue function


# Thanks to:
# http://www.rabbitmq.com/tutorials/tutorial-one-python.html
#from DepartureTimes.communication.util import ensure_data_events_are_processed


def send(queue_name, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

 #   ensure_data_events_are_processed(channel)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=data,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()
