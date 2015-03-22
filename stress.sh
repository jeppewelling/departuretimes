# echo "1 Client"
# python -m Stress.stress_send_query

# echo "2 Clients"
# python -m Stress.stress_send_query & 
# python -m Stress.stress_send_query &
# wait

# echo "3 Clients"
# python -m Stress.stress_send_query & 
# python -m Stress.stress_send_query & 
# python -m Stress.stress_send_query &
# wait

echo "4 Clients"
python -m Stress.stress_send_query & 
python -m Stress.stress_send_query & 
python -m Stress.stress_send_query &
python -m Stress.stress_send_query & 
wait


echo "Stress complete"
