
# Given the slope of the average line of the search times and the sum of the times above the baseline,
# return a number of Query workers.


def number_of_workers(slope, integrated_sum):
    # 'a' indicates how sensitive the load balancer should be toward accelerations in search times
    a = 150

    # 'b' indicates how sensitive the load balancer should be toward a continuous offset in search
    # # time compared with the baseline search time
    b = 0.0015

    s = slope * a
    i = integrated_sum * b
    return s + i

if __name__ == '__main__':
    print "Average 3.25 ms: w=%s" % number_of_workers(0.000917663735062, 2498)

    print "Average 4.3 ms: w=%s" % number_of_workers(0.00143696665932, 3552)



    print "Average 3.5 ms: w=%s" % number_of_workers(0.000170943219641, 2755)

    print "Average 2.6 ms: w=%s" % number_of_workers(0.00117639279161, 1874)

    print "Average 2.9 ms: w=%s" % number_of_workers(0.00336239276738, 2161)

    print "Average 2.01 ms: w=%s" % number_of_workers(-0.0036364307122, 1261)
