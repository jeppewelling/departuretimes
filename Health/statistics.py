from __future__ import division

from Health.data import V, TS
from Loadbalancer.main import worker_acceleration, LoadBalancer


# For each measure point we keep a running regression line in the scope of the last x-amount of points.
# When x-points has been collected the current trend of the system is evaluated.
# The result of the evaluation is passed on to the load balancer who decides if more workers should be added or not.
# As of now, the statistics are only used by  the search time calculations.
class Statistics(object):
    def __init__(self, mean_length, baseline):
        # Lets set the base line a bit higher than measured.
        # This way we will get a negative value of the summed search
        # times when compared with the base line.
        self.optimal_search_time_ms = baseline #
        self.load_balancer = LoadBalancer()

        self.message_count = 0
        self.mean_length = mean_length

        # The slope of the linear regression line through the c previous points
        self.current_slope = 0
        # the sum of the measured values minus the optimal value.
        self.current_integrate = 0

        self.mean_x_sum = 0
        self.mean_y_sum = 0
        self.mean_x = 0
        self.mean_y = 0
        self.regression_upper = 0
        self.regression_lower = 0


    def print_report(self, m):
        print "Baseline search time: %s ms" % self.optimal_search_time_ms
        print "cnt: %s" % self.message_count
        print "Average search time: %s ms" % self.mean_y
        print "Regression line for the last %s points:" % self.mean_length
        print "y = %sx" % (self.current_slope)
        print "integrate=%s" % self.current_integrate
        print "point=%s" % m
        print ""
        print "Workers: %s" % worker_acceleration(self.current_slope, self.current_integrate)
        print ""
        print "-----------------------------------------------------------"

    def maybe_reset(self):
        # Reset as the first action in the 'next period'
        if self.message_count == self.mean_length:
            self.current_slope = 0
            self.current_integrate = 0
            self.mean_x_sum = 0
            self.mean_y_sum = 0
            self.mean_x = 0
            self.mean_y = 0
            self.regression_upper = 0
            self.regression_lower = 0
            self.message_count = 0

    # Called every time a new measure is received
    def on_new_measure(self, m):
        print "on_new_measure: %s" % m
        self.maybe_reset()
        self.message_count += 1
        self.update_mean(m)
        self.update_integrate(m)

        if self.message_count == self.mean_length and self.message_count > 0:
            self.current_slope, _ = self.linear_regression_from_state()
            self.load_balancer.on_update_workers(self.current_slope, self.current_integrate)
            self.print_report(m)





    def update_integrate(self, p):
        diff = p[V] - self.optimal_search_time_ms
        self.current_integrate += diff


    def update_mean(self, p):
        n = self.message_count
        x_i = p[TS]
        y_i = p[V]
        self.mean_y_sum += y_i
        self.mean_x_sum += x_i
        self.mean_x = self.mean_x_sum / n
        self.mean_y = self.mean_y_sum / n

        self.regression_upper = self.regression_upper + x_i * y_i
        self.regression_lower = self.regression_lower + x_i * x_i


    def linear_regression_from_state(self):
        n = self.mean_length
        upper = self.regression_upper - n * self.mean_x * self.mean_y
        lower = self.regression_lower - n * self.mean_x * self.mean_x

        if self.regression_lower == 0: return 0, 0
        if lower == 0: return 0, 0

        a = upper / lower
        b = self.mean_y - a * self.mean_x
        return a, b
