# EXERCISE 1. COMMUNICATION SERVICES AND SECURITY

# EXERCISE 2

# EXERCISE 3

In the folder ex3 are contained all the python scripts used to complete this assignment. Below there is explained the folder structure along with how to run the different section.
However, there is the option to run all the code by:
````
make all
````

## ITEM 1

## Folder Structure

The folders inside the module ex3/item1 are:

- agent_results: contains the results of running an agent with run_simulations.py
- agents: our python implementation of both the TCP RFC793 and Reno agents
- ns_simulations: files used to run simulations in ns along with the results 

## Run the Agents
To run a simulation with the agent 'RFC793 with slow start' and get a plot of the timeouts and congestion window comparisons, you can run:
````
make run_tcp_rfc793
````
Likewise, to use the reno agent, you can run:
````
make run_reno
````

# ITEM 2

To show an example of fast retransmissions, we made a plot of the cw obtained by the Reno simulation and get an idea of the points where fast retransmission occurred. This plot can be generated by running:
````
make plot_reno_cwnd
````

# ITEM 3

To get the sequence numbers of the packets used to update the reno simulation, you can run:
````
make get_reno_rtt_seqs
````
This will execute the script run_simulation.py with the reno agent in debug mode, so it will print the rtt sequences used to update the Timeout and it will save this in the file rtt_seq_nums.txt

# ITEM 4

TODO

# ITEM 5

To show an example of partial acks, we made a plot of the cw obtained by the NewReno simulation and get an idea of the points where partial acks could have occurred. This plot can be generated by running:
````
make plot_new_reno_cwnd
````

# ITEM 6

TODO: explicar throughput?

In order to compare the congestion window of TCP reno with and without RED, we have generated a plot by running:
````
plot_tcp_red_comparisons
````