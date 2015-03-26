set terminal png transparent nocrop enhanced size 450,320 font "arial,8"
set output 'search_time_2.png'
set key inside left top vertical Left noreverse enhanced autotitle nobox
set label 1 "min" at 2.07944, graph 0.1, 0 centre norotate back nopoint offset character 0, -1, 0
set label 2 "max" at 2.30259, graph 0.9, 0 centre norotate back nopoint offset character 0, 1, 0
set arrow 1 from 2.07944, graph 0.1, 0 to 2.07944, 2.20087, 0.00000 head filled
set arrow 2 from 2.30259, graph 0.9, 0 to 2.30259, 3.13972, 0.00000 head filled
set offsets 0, 0, 0.5, 0.5
set style data lines
set title "Use of stats command to find min/max/mean before plotting\nTwo data columns"
set autoscale rfixmin
set autoscale rfixmax
set autoscale tfixmin
set autoscale tfixmax
set autoscale ufixmin
set autoscale ufixmax
set autoscale vfixmin
set autoscale vfixmax
set autoscale xfixmin
set autoscale xfixmax
set autoscale x2fixmin
set autoscale x2fixmax
set autoscale yfixmin
set autoscale yfixmax
set autoscale y2fixmin
set autoscale y2fixmax
set autoscale zfixmin
set autoscale zfixmax
set autoscale cbfixmin
set autoscale cbfixmax
f(x) = log(1+x)
A_records = 20.0
A_invalid = 0.0
A_blank = 1.0
A_blocks = 1.0
A_outofrange = 0.0
A_columns = 11.0
A_mean = 2.54077965
A_stddev = 0.222745079388137
A_ssd = 0.228531629485718
A_skewness = 0.978323019217487
A_kurtosis = 3.60561959806089
A_adev = 0.0
A_mean_err = 0.0498073139165462
A_stddev_err = 0.0352190894230769
A_skewness_err = 0.547722557505166
A_kurtosis_err = 1.09544511501033
A_sum = 50.815593
A_sumsq = 130.103532004915
A_min = 2.20087
A_max = 3.139718
A_median = 2.4609945
A_lo_quartile = 2.3865975
A_up_quartile = 2.6562155
A_index_min = 7.0
A_index_max = 9.0
x = 0.0
GPFUN_f = "f(x) = log(1+x)"
B_records = 20.0
B_invalid = 0.0
B_blank = 1.0
B_blocks = 1.0
B_outofrange = 0.0
B_columns = 11.0
B_mean_x = 2.11678082303767
B_stddev_x = 0.792134394132666
B_ssd_x = 0.812712740322205
B_skewness_x = -1.11744391283858
B_kurtosis_x = 3.52503054370255
B_adev_x = 0.2
B_mean_err_x = 0.177126635259625
B_stddev_err_x = 0.125247444920837
B_skewness_err_x = 0.547722557505166
B_kurtosis_err_x = 1.09544511501033
B_sum_x = 42.3356164607535
B_sumsq_x = 102.16475902296
B_min_x = 0.0
B_max_x = 2.99573227355399
B_median_x = 2.35024018289621
B_lo_quartile_x = 1.70059869083108
B_up_quartile_x = 2.740319461671
B_index_min_x = 0.0
B_index_max_x = 19.0
B_mean_y = 2.54077965
B_stddev_y = 0.222745079388137
B_ssd_y = 0.228531629485718
B_skewness_y = 0.978323019217487
B_kurtosis_y = 3.60561959806089
B_adev_y = 0.0
B_mean_err_y = 0.0498073139165462
B_stddev_err_y = 0.0352190894230769
B_skewness_err_y = 0.547722557505166
B_kurtosis_err_y = 1.09544511501033
B_sum_y = 50.815593
B_sumsq_y = 130.103532004915
B_min_y = 2.20087
B_max_y = 3.139718
B_median_y = 2.4609945
B_lo_quartile_y = 2.3865975
B_up_quartile_y = 2.6562155
B_index_min_y = 7.0
B_index_max_y = 9.0
B_slope = -0.066943671163917
B_intercept = 2.68248472934352
B_slope_err = 0.0643729477667789
B_intercept_err = 0.145491947243556
B_correlation = -0.238067590736956
B_sumxy = 106.725360630742
B_pos_min_y = 2.07944154167984
B_pos_max_y = 2.30258509299405
## Last datafile plotted: "health_SearchTime.log"
plot 'health_SearchTime.log' index 1 using (f($0)):2 title "  Data" lw 2,      B_mean_y title "  Mean",      B_slope * x + B_intercept title "Linear fit"