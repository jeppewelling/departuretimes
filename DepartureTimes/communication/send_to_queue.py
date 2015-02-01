import pika

# A generic send-to-queue function

# Thanks to:
# http://www.rabbitmq.com/tutorials/tutorial-one-python.html
def send(queue_name, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=data)
    connection.close()