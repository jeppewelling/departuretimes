from __future__ import division
# a generic sum function with a selector closure
from twisted.trial import unittest
from Health.data import TS, V, make_fixed_measure
from Health.statistics import Statistics



def sum_(func, list):
    return reduce(lambda acc, x: func(x) + acc, list, 0)


def mean(func, points):
    if len(points) == 0: return 0
    return sum_(func, points) / len(points)


# Linear regression over points

# a = Sum^n_i{x_i * y_i - n * xl * yl } / Sum^n_i{x^2_i - n * xl^2 }
#
# Where xl and yl are the mean values of x and y
# Reference implementation
# Extremely important to import:
# from __future__ import division
def linear_regression(points_lst):
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



class TestStatistics(unittest.TestCase):

    def setUp(self):
        return None


    def test_linear_regression_state(self):
        ps = [make_fixed_measure(1,2223),
              make_fixed_measure(1,2556),
              make_fixed_measure(1,2455),
              make_fixed_measure(2,4898)]

        a, b = linear_regression(ps)

        s = Statistics(len(ps), 4)
        for p in ps:
            s.on_new_measure(p)

        aa, bb = s.linear_regression_from_state()

        self.assertEqual(aa, a)
        self.assertEqual(bb, b)


    def test_linear_regression_state_modulo(self):
        ps1 = [make_fixed_measure(1,2223),
              make_fixed_measure(1,2556),
              make_fixed_measure(1,2455),
              make_fixed_measure(2,4898),

              make_fixed_measure(1,2223),
              make_fixed_measure(1,2556),
              make_fixed_measure(1,2455),
              make_fixed_measure(2,4898)]

        ps2 = [make_fixed_measure(1,2223),
              make_fixed_measure(1,2556),
              make_fixed_measure(1,2455),
              make_fixed_measure(2,4898)]

        a, b = linear_regression(ps2)

        mean_length = 4
        baseline = 4
        s = Statistics(mean_length, baseline)
        for p in ps1:
            s.on_new_measure(p)

        aa, bb = s.linear_regression_from_state()

        self.assertEqual(aa, a)
        self.assertEqual(bb, b)

