echo "2 Clients"
python -m Stress.stress_send_query & 
python -m Stress.stress_send_query &
