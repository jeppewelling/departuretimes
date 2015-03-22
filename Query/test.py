#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='test1',
                         type='fanout')

channel.exchange_declare(exchange='test2',
                         type='fanout')


def callback(ch, method, properties, body):
    print " [x] %r" % (body,)


result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='test1',
                   queue=queue_name)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)



result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='test2',
                   queue=queue_name)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)


print ' [*] Waiting for logs. To exit press CTRL+C'



channel.start_consuming()