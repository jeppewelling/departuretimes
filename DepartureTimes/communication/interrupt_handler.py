import signal
import sys
from time import sleep
from contextlib import contextmanager

received_signal = False
processing_callback = False


# Handle signals from the outside environment i.e. stop start.
def signal_handler(signal, frame):
    global received_signal
    received_signal = True
    if not processing_callback:
        shutdown()


@contextmanager
def block_signals():
    global processing_callback
    processing_callback = True
    try:
        yield
    finally:
        processing_callback = False
        if received_signal:
            shutdown()


def shutdown():
    print "Received terminate signal, shutting down."
    sys.exit()


restart_wait_time_seconds = 10


# A top level exception handler to keep the application alive on
# error. E.g. if rmq is restarted.
def exception_handler(main_f):
    # Add the signal events
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        main_f()
    except Exception as ex:
        print type(ex)     # the exception instance
        print ex.args      # arguments stored in .args
        print "Encountered an error"
        print ex
        print "lets start again in %s seconds ;-)" % restart_wait_time_seconds
        sleep(restart_wait_time_seconds)
        exception_handler(main_f)


@contextmanager
def message_exception_handler(body):
    try:
        yield
    except Exception as ex:
        print " [Exception] Input error: %s" % body
        print " [Exception] %s" % ex.message


@contextmanager
def rpc_exception_handler():
    try:
        yield
    except Exception as ex:
        print " [Exception] in RMQ RPC context. Probably a connection was closed: %s" % ex
