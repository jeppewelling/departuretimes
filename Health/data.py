import time

__author__ = 'jwh'


# Health   ::= [<Type> <Measure>]
# Type     ::= SearchTime | ...
# Measure  ::= [<TimeStamp> <decimal>]

M = u'Measure'
T = u'Type'
TS = u'TimeStamp'
V = u'Value'


def now_ms():
    return float(time.time() * 1000)

initial_time = now_ms()

def make_measure( v):
    ts = now_ms() - initial_time
    return {TS: ts, V: v}


def make_health_state(t, m):
    return {T: t, M: m, }


