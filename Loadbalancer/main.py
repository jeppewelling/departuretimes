
# Given the slope of the average line of the search times and the sum of the times above the baseline,
# return a number of Query workers.
from Queue import Queue
import os
import signal
import time
import subprocess
import math

WORKER_PATH = "/home/jwh/projects/departuretimes/run_query.py"



class LoadBalancer(object):
    def __init__(self):
        self.process_manager = ProcessManager()

    def on_update_workers(self, slope, integrated_sum):
        n = number_of_workers(slope, integrated_sum)
        if n < 0:
            self.remove_n_workers(abs(n))

        if n > 0:
            self.add_n_workers(n)

    def remove_n_workers(self, n):
        print "Killing %s workers" % n
        for _ in xrange(n):
            self.process_manager.kill_process()

    def add_n_workers(self, n):
        print "spawning %s new workers" % n
        for _ in xrange(n):
            self.process_manager.spawn_process(WORKER_PATH)




class ProcessManager(object):

    def __init__(self):
        self.processes = Queue()

    def spawn_process(self, path):
        process = subprocess.Popen(['python', path], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.put(process)
        pid = process.pid
        print "spawned process: %s" % pid


    def kill_process(self):
        if self.processes.empty():
            return

        self.kill_process_by(self.processes.get())

    @staticmethod
    def kill_process_by(process):
        process.terminate()



def number_of_workers(slope, integrated_sum):
    # 'a' indicates how sensitive the load balancer should be toward accelerations in search times
    a = 500

    # 'b' indicates how sensitive the load balancer should be toward a continuous offset in search
    # # time compared with the baseline search time
    b = 0.10

    s = slope * a

    i = 0
    if integrated_sum > 0:
        i = math.log10(integrated_sum) * b
    if integrated_sum < 0:
        i = -math.log10(-integrated_sum) * b * 1.8

    print "i=%s, s=%s" % (i, s)
    return int(round(s + i))


if __name__ == '__main__':
    pm = ProcessManager()
    pm.spawn_process(WORKER_PATH)
    time.sleep(5)
    pm.kill_process()

    print "Average 3.25 ms: w=%s" % number_of_workers(0.000917663735062, 2498)

    print "Average 4.3 ms: w=%s" % number_of_workers(0.00143696665932, 3552)


    print "Average 3.5 ms: w=%s" % number_of_workers(0.000170943219641, 2755)

    print "Average 2.6 ms: w=%s" % number_of_workers(0.00117639279161, 1874)

    print "Average 2.9 ms: w=%s" % number_of_workers(0.00336239276738, 2161)

    print "Average 2.01 ms: w=%s" % number_of_workers(-0.0036364307122, 1261)

    print "Average 1.26 ms: w=%s" % number_of_workers(-0.0036364307122, 138.6)

    print "Average x ms: w=%s" % number_of_workers(-.0000620173780578, 505.23)

    print "Average x ms: w=%s" % number_of_workers(0.0039612244549, 1884)

    print "Average 0.94 ms: w=%s" % number_of_workers(0.000202213190403, -132)






