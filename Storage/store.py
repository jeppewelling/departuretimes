import pika
import json

queue_name = "train_departures"


# Thanks to:
# http://www.rabbitmq.com/tutorials/tutorial-one-python.html
def receive_imports():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    
    print ' [*] Waiting for messages. To exit press CTRL+C'
    
    def callback(ch, method, properties, body):
        print " [x] Received %r" % (json.loads(body),)
        
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
        
    channel.start_consuming()

if __name__ == "__main__":
    receive_imports()
