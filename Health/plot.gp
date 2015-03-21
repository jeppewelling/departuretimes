set term png
set output "search_time.png"
set xdata time
set timefmt "%s"
plot "../health_SearchTime.log" using 1:2 with lines
