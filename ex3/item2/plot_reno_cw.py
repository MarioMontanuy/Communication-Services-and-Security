import sys
import os
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
from ex3.item1.show_simulation_results import load_file, get_reno_cw


def plot_cw(agent, ns_cw):
    ns_times, ns_cw = zip(*ns_cw)

    # Plot timeouts using matplotlib
    plt.plot(ns_times, ns_cw, label="NS")
    plt.xlabel("Time")
    plt.ylabel("Congestion Window")
    plt.title("Agent: " + agent)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    agent = "reno"
    ns_cw_file = load_file(f"ex3/item1/ns_simulations/{agent}/cw.tcp_{agent}_ss")
    ns_cw = get_reno_cw(ns_cw_file)
    plot_cw(agent, ns_cw)
