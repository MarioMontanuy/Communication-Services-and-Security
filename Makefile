
run_tcp_rfc793:
	echo "Running TCP RFC 793"
	python ex3/item1/run_simulation.py tcp_rfc793

run_reno:
	echo "Running TCP Reno"
	python ex3/item1/run_simulation.py reno

plot_reno_cwnd:
	python ./ex3/item2/plot_reno_cw.py

get_reno_rtt_seqs:
	echo "Running TCP Reno"
	python ex3/item1/run_simulation.py reno --d > ./ex3/item3/rtt_seq_nums.txt

plot_new_reno_cwnd:
	python ./ex3/item5/plot_new_reno_cw.py

plot_tcp_red_comparisons:
	python ./ex3/item6/plot_tcp_red_comparisons.py

all: run_tcp_rfc793 run_reno plot_reno_cwnd get_reno_rtt_seqs plot_new_reno_cwnd plot_tcp_red_comparisons