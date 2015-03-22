from DepartureTimes.communication.publish import Publish
from DepartureTimes.communication.queues import departures_exchange


pub = Publish(departures_exchange)


def publish_departures(departures):
    pub.publish(departures)


def close():
    pub.close()