set term png size 2000,640
set output "health_SearchTime.png"


plot "health_SearchTime.log" u 1:2	#To get the max and min value
ymax=GPVAL_DATA_Y_MAX
ymin=GPVAL_DATA_Y_MIN
ylen=ymax-ymin
xmax=GPVAL_DATA_X_MAX
xmin=GPVAL_DATA_X_MIN
xlen=xmax-xmin
#plot
set term png
set output "health_SearchTime.png"
set xrange [xmin:xmax]
set yrange [ymin-0.5*ylen:ymax+0.5*ylen]
set xlabel "Time (ms)"
set ylabel "Time (ms)"

plot "health_SearchTime.log" u 1:2 w p pt 7 ps 0.5 notitle,\
     "health_SearchTime.log" u (xmax+0.1*xlen):($2):(1.1*xlen)\
     smooth unique w xerrorbars notitle,\
     ymax w l lt 3 notitle,\
     ymin w l lt 3 notitle
#plot raw data, mean value, max


