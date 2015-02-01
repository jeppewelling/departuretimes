import pika

# A generic queue reader

def read(queue_name, message_handler):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    print ' [*] Waiting for messages on queue: %r' % (queue_name)
    
    def callback(ch, method, properties, body):
        message_handler(body)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()
