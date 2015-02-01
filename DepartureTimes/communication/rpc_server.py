import pika 
import json

# A generic RPC server

class RpcServer(object):
    def __init__(self, queue_name, response_handler):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.queue_name = queue_name
        self.response_handler = response_handler

        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=queue_name)

        print " [x] Server: Awaiting RPC requests on queue: %r" % queue_name
        self.channel.start_consuming()


    def on_request(self, ch, method, props, body):
        response = self.response_handler(body)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id = props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
