
run_tcp_rfc793:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "Running TCP RFC 793"
	python ex3/item1/run_simulation.py tcp_rfc793

run_reno:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "Running TCP Reno"
	python ex3/item1/run_simulation.py reno

plot_reno_cwnd:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "Plotting TCP Reno Congestion Window"
	python ./ex3/item2/plot_reno_cw.py

get_reno_rtt_seqs:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "Running TCP Reno"
	python ex3/item1/run_simulation.py reno --d > ./ex3/item3/rtt_seq_nums.txt

get_reno_throughput:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "TCP Reno Throughput"
	python ex3/item4/throughput.py ./ex3/item4/reno/sor.tcp_Reno_ss

get_new_reno_throughput:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "TCP New Reno Throughput"
	python ex3/item4/throughput.py ./ex3/item4/newreno/sor.tcp_Newreno_ss

plot_new_reno_cwnd:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "Plotting TCP New Reno Congestion Window"
	python ./ex3/item5/plot_new_reno_cw.py

get_reno_wait_true_throughput:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "TCP Reno Throughput + RED with Wait True"
	python ex3/item6/throughput.py ./ex3/item6/wait_true/sor.tcp_Reno_item6_ss

get_reno_wait_false_throughput:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "TCP Reno Throughput + RED with Wait False"
	python ex3/item6/throughput.py ./ex3/item6/wait_false/sor.tcp_Reno_item6_ss

plot_tcp_red_comparisons:
	@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	echo "Plotting TCP Reno and RED Comparisons"
	python ./ex3/item6/plot_tcp_red_comparisons.py

all: run_tcp_rfc793 run_reno plot_reno_cwnd get_reno_rtt_seqs get_reno_throughput get_new_reno_throughput plot_new_reno_cwnd get_reno_wait_true_throughput get_reno_wait_false_throughput plot_tcp_red_comparisons
