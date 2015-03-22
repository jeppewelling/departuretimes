set term png
set output "health_FetchDepartureTime.png"
set xdata time
set timefmt "%s"
plot "../health_FetchDeparturesTime.log" using 1:2 with lines
