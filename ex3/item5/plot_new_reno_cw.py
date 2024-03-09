import sys
import os
sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
from ex3.item1.show_simulation_results import load_file, get_reno_cw
from ex3.item2.plot_reno_cw import plot_cw

if __name__ == "__main__":
    agent = "Newreno"
    ns_cw_file = load_file(f"ex3/item4/newreno/cw.tcp_{agent}_ss")
    ns_cw = get_reno_cw(ns_cw_file)
    plot_cw(agent, ns_cw)