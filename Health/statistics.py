from __future__ import division
from Queue import Queue

from Health.data import V, TS, make_measure
from Loadbalancer.main import number_of_workers, LoadBalancer
from Stress.stress_send_query import baseline_average_search_time_ms


class Statistics(object):
    def __init__(self):
        # Lets set the base line a bit higher than measured.
        # This way we will get a negative value of the summed integration
        # when the search time is optimal.
        self.optimal_search_time_ms = baseline_average_search_time_ms(2000) * 2
        print "Baseline search time: %s ms" % self.optimal_search_time_ms

        self.load_balancer = LoadBalancer()

        self.message_count = 0
        self.mean_x_sum = 0
        self.mean_y_sum = 0
        self.mean_x = 0
        self.mean_y = 0
        self.mean_length = 2000
        self.points = Queue(self.mean_length)

        # y = ax + b
        # where a is slope and b is offset
        self.current_slope = 0
        self.current_offset = 0

        # the sum of the measured values minus the optimal value.
        self.current_integrate = 0

    def print_report(self, m):
            a = self.current_slope
            b = self.current_offset
            i = self.current_integrate

            print "cnt: %s" % self.message_count
            print "Average search time: %s ms" % self.mean_y
            print "Average regression line for the last %s points" % self.mean_length
            print "y = %sx + %s" % (a, b)
            print "integrate=%s" % i
            print "point=%s" % m
            print ""
            print "Workers: %s" % number_of_workers(self.current_slope, self.current_integrate)
            print ""
            print "-----------------------------------------------------------"


    # Called every time a new measure is received
    def on_new_measure(self, m):
        self.message_count += 1

        if self.message_count % self.mean_length == 0:
            points_lst = list(self.points.queue)
            self.update_slope(points_lst)


            self.load_balancer.on_update_workers(self.current_slope, self.current_integrate)
            self.print_report(m)



        self.update_points(m)
        self.update_mean(m)

        self.update_integrate(m)

    def update_mean(self, measure):
        if self.message_count % self.mean_length == 0:
            self.mean_x_sum = 0
            self.mean_y_sum = 0
            self.mean_x = 0
            self.mean_y = 0
            self.current_integrate = 0

        self.mean_y_sum += measure[V]
        self.mean_x_sum += measure[TS]

        self.mean_x = self.mean_x_sum / self.mean_length
        self.mean_y = self.mean_y_sum / self.mean_length

    def update_integrate(self, p):
        diff = p[V] - self.optimal_search_time_ms
        self.current_integrate += diff


    def update_points(self, measure):
        if self.points.full():
            self.points.get()
        self.points.put(measure)

    def update_slope(self, points_lst):
        self.current_slope, self.current_offset = slope(points_lst)


# a generic sum function with a selector closure
def sum_(func, list):
    return reduce(lambda acc, x: func(x) + acc, list, 0)


def mean(func, points):
    if len(points) == 0: return 0
    return sum_(func, points) / len(points)


# Linear regression over points

# a = Sum^n_i{x_i * y_i - n * xl * yl } / Sum^n_i{x^2_i - n * xl^2 }
#
# Where xl and yl are the mean values of x and y
def slope(points_lst):
    n = len(points_lst)
    xl = mean(lambda m: m[TS], points_lst)
    yl = mean(lambda m: m[V], points_lst)
    upper = 0
    lower = 0
    for p in points_lst:
        x_i = p[TS]
        y_i = p[V]

        upper = upper + x_i * y_i
        lower = lower + x_i * x_i

    upper = upper - n * xl * yl
    lower = lower - n * xl * xl
    if lower == 0: return 0, 0
    a = upper / lower
    b = yl - a * xl

    return a, b



def human_readable_state(a):
    if a > 0:
        return "Slower"
    if a < 0:
        return "Faster"
    return "Steady"





if __name__ == '__main__':
    ps = [make_measure(1, 1),
          make_measure(2, 1),
          make_measure(3, 1),
          make_measure(4, 2)]

    a, b = slope(ps)

    print "y = %sx + %s\ndiff=%s" % (a, b, a)

