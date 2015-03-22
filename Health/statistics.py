from __future__ import division
from Queue import Queue
from Health.data import V, TS, make_measure


optimal_search_time_ms = 2
cnt = 0


def human_readable_state(a):
    if a > 0:
        return "Slower"
    if a < 0:
        return "Faster"
    return "Steady"



def on_new_measure(m):
    global cnt, points, mean_y, mean_length, current_slope, current_offset, current_integrate
    cnt += 1

    if (cnt + 1) % mean_length == 0:
        a = current_slope
        b = current_offset
        i = current_integrate

        print "Average search time: %s ms" % mean_y
        print "Average regression line for the last %s points" % mean_length
        print "y = %sx + %s" % (a, b)
        print "integrate=%s" % i
        print ""
        print "Prediction: %s" % human_readable_state(a)
        print ""
        print "-----------------------------------------------------------"

    points_lst = list(points.queue)
    update_points(m)
    update_mean(m)
    update_slope(points_lst)
    update_integrate(points_lst)




mean_x_sum = 0
mean_y_sum = 0
mean_x = 0
mean_y = 0
mean_length = 200


def update_mean(measure):
    global mean_x, mean_y, mean_x_sum, mean_y_sum, mean_length, cnt
    if cnt % mean_length == 0:
        mean_x_sum = 0
        mean_y_sum = 0
        mean_x = 0
        mean_y = 0

    mean_y_sum += measure[V]
    mean_x_sum += measure[TS]

    mean_x = mean_x_sum / mean_length
    mean_y = mean_y_sum / mean_length


# Linear regression over points

# a = Sum^n_i{x_i * y_i - n * xl * yl } / Sum^n_i{x^2_i - n * xl^2 }
#
# Where xl and yl are the mean values of x and y

points = Queue(mean_length)


def update_points(measure):
    global points
    if points.full():
        points.get()
    points.put(measure)

# y = ax + b
# where a is slope and b is offset
current_slope = 0
current_offset = 0


def update_slope(points_lst):
    global current_slope, current_offset
    current_slope, current_offset = slope(points_lst)


# a more generic sum function
def sum_(func, list):
    return reduce(lambda acc, x: func(x) + acc, list, 0)


def mean(func, points):
    if len(points) == 0: return 0
    return sum_(func, points) / len(points)


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


current_integrate = 0


def update_integrate(points_lst):
    global current_integrate, current_slope, current_offset, optimal_search_time_ms
    current_integrate = integrate(points_lst, current_slope, current_offset, optimal_search_time_ms)


def integrate(points_lst, a, b, y_optimal):
    if len(points_lst) < 2:
        return 0

    first_x = points_lst[0][TS]
    last_x = points_lst[len(points_lst) - 1][TS]

    # Integrate: Calculate the area under the aggression line
    # above the optimal search line.
    # i.e. the triangle spanned by s, t, u below:
    #
    # ^
    # |           u       (drifting search times)
    # |         / |
    # |       /   |
    # |     /     |
    # |----s------t------- optimal search time
    # |
    # -------------------------------> x
    #

    # Calculate the aggression lines intersection with the y_optimal
    # y = ax + b
    # y_optimal = ax + b
    # x = (y_optimal - b) / a

    # If a is zero we have a box area
    if a == 0:
        return (last_x - first_x) * (b - y_optimal)

    s_x = (y_optimal - b) / a

    u_x = last_x
    u_y = a * u_x + b

    t_x = u_x
    t_y = y_optimal

    st = t_x - s_x
    tu = u_y - t_y
    area = st * tu * 0.5

    return area


if __name__ == '__main__':
    ps = [make_measure(1, 1),
          make_measure(2, 1),
          make_measure(3, 1),
          make_measure(4, 2)]

    a, b = slope(ps)
    i = integrate(ps, a, b)

    print "y = %sx + %s\ndiff=%s\nintegrate=%s" % (a, b, a, i)