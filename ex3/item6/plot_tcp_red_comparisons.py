import sys
import os
sys.path.append(os.getcwd())
from ex3.item1.show_simulation_results import load_file, get_reno_cw
from ex3.item1 import utils
import matplotlib.pyplot as plt

def plot_reno_comparison(reno_cw, reno_red_wait_false_cw, reno_red_wait_true_cw):
    reno_times, reno_cw = zip(*reno_cw)
    reno_red_wait_false_times, reno_red_wait_false_cw = zip(*reno_red_wait_false_cw)
    reno_red_wait_true_times, reno_red_wait_true_cw = zip(*reno_red_wait_true_cw)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    ax1.plot(reno_times, reno_cw, label="Reno")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Congestion Window")
    ax1.legend()
    
    ax2.plot(reno_red_wait_false_times, reno_red_wait_false_cw, label="Reno + RED + Wait False", color="red")
    ax2.plot(reno_red_wait_true_times, reno_red_wait_true_cw, label="Reno + RED + Wait True", color="green")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Congestion Window")
    ax2.legend()

    plt.show()

if __name__ == "__main__":
    ns_cw_results_reno = load_file(utils.get_agent_ns_cw("reno"))
    ns_cw_results_reno_red_wait_false = load_file(utils.get_agent_ns_cw("reno+red+wait_false"))
    ns_cw_results_reno_red_wait_true = load_file(utils.get_agent_ns_cw("reno+red+wait_true"))
    plot_reno_comparison(get_reno_cw(ns_cw_results_reno), get_reno_cw(ns_cw_results_reno_red_wait_false), get_reno_cw(ns_cw_results_reno_red_wait_true))