import json
import pika
import time
from queues import health_queue_name

# The RMQ setup for sending messages to the health service

SearchTime = "SearchTime"
FetchStationsTime = "FetchStationsTime"
FetchDeparturesTime = "FetchDeparturesTime"


class HealthClient(object):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = health_queue_name
        self.begin_search_time = 0

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        # Takes a relative long time to do...
        # Maybe we should consider moving this out in a separate method
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def begin_search_time_measure(self):
        self.begin_search_time = now_ms()

    def end_search_time_measure(self):
        self.connect();
        diff = now_ms() - self.begin_search_time
        self.send_health_status(SearchTime, diff)
        self.close()

    def send_health_status(self, kind, measured_value):
        m = make_measure(measured_value)
        health = make_health_state(kind, m)
        self.send(json.dumps(health))

    def send(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=data,
                                   properties=pika.BasicProperties(
                                       delivery_mode=1,  # make message non-persistent
                                   ))

    def close(self):
        self.connection.close()


def now_ms():
    return float(time.time() * 1000)

initial_time = now_ms()

# Health   ::= [<Type> <Measure>]
# Type     ::= SearchTime | ...
# Measure  ::= [<TimeStamp> <decimal>]

M = u'Measure'
T = u'Type'
TS = u'TimeStamp'
V = u'Value'

def make_measure( v):
    ts = now_ms() - initial_time
    return {TS: ts, V: v}

def make_health_state(t, m):
    return {T: t, M: m, }
