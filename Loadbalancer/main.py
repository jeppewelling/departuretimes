# Given the slope of the average line of the search times and the sum of the times above the baseline,
# return a number of QueryDepartures workers.
from Queue import Queue
import time
import subprocess
import math
from config import QUERY_WORKER_PATH

WORKER_PATH = QUERY_WORKER_PATH


class LoadBalancer(object):
    def __init__(self):
        self.process_manager = ProcessManager()

    def on_update_workers(self, slope, integrated_sum):
        a = worker_acceleration(slope, integrated_sum)
        if a < 0:
            self.remove_worker()

        if a > 0:
            self.add_n_workers()

    def remove_worker(self):
        print "Killing 1 worker"
        self.process_manager.kill_process()

    def add_n_workers(self):
        print "spawning 1 new worker"
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


# Defines if the number of workers should be added, removed or stay the same
# -1: remove a single worker
#  0: keep the number of workers the same
#  1: add another worker.
# The constants defined below are derived from a set of tests performed on my developer machine.
def worker_acceleration(slope, integrated_sum):
    # 'a' indicates how sensitive the load balancer should be toward accelerations in search times
    a = 500

    # 'b' indicates how sensitive the load balancer should be toward a continuous offset in search
    # # time compared with the baseline search time
    b = 0.10

    s = slope * a

    i = 0
    if integrated_sum > 0:
        i = math.log10(integrated_sum) * b

    # Help decreasing the amount of workers by multiplying with a the constant
    b_decrease = 1.8
    if integrated_sum < 0:
        i = -math.log10(-integrated_sum) * b * b_decrease

    print "i=%s, s=%s" % (i, s)

    out = int(round(s + i))

    if out > 0:
        return 1
    if out < 0:
        return -1
    return 0


if __name__ == '__main__':
    print "Average 3.25 ms: w=%s" % worker_acceleration(0.000917663735062, 2498)

    print "Average 4.3 ms: w=%s" % worker_acceleration(0.00143696665932, 3552)

    print "Average 3.5 ms: w=%s" % worker_acceleration(0.000170943219641, 2755)

    print "Average 2.6 ms: w=%s" % worker_acceleration(0.00117639279161, 1874)

    print "Average 2.9 ms: w=%s" % worker_acceleration(0.00336239276738, 2161)

    print "Average 2.01 ms: w=%s" % worker_acceleration(-0.0036364307122, 1261)

    print "Average 1.26 ms: w=%s" % worker_acceleration(-0.0036364307122, 138.6)

    print "Average x ms: w=%s" % worker_acceleration(-.0000620173780578, 505.23)

    print "Average x ms: w=%s" % worker_acceleration(0.0039612244549, 1884)

    print "Average 0.94 ms: w=%s" % worker_acceleration(0.000202213190403, -132)






