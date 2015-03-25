# Reads from the queue and immediately sends back an answer to the sender.
import pika
from DepartureTimes.communication.interrupt_handler import block_signals, rpc_exception_handler



def add_rpc_server_queue(channel, queue_name, message_handler):
    channel.queue_declare(queue=queue_name)

    # The message handler calls back to the sender.
    def message_handler_callback(ch, method, properties, body):
        with block_signals():
            response = message_handler(body)
            ch.basic_publish(exchange='',
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(
                                 correlation_id=properties.correlation_id),
                             body=response)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    with rpc_exception_handler():
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(message_handler_callback,
                              queue=queue_name)


#
# message_counter = 0
#
# # A minor hack to keep the RMQ connection alive, see:
# # https://github.com/pika/pika/issues/397
# def ensure_data_events_are_processed(channel):
#     global message_counter
#     message_counter += 1
#     if message_counter % 100 == 0:
#         channel.proces_data_events()
