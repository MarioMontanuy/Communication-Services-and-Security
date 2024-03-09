import os, sys
sys.path.append(os.getcwd())

import matplotlib.pyplot as plt
from ex3.item1 import utils


def load_file(file):
    with open(file, "r") as file:
        return file.readlines()


def get_timeouts_and_cw(results):
    timeouts = []
    cw = []
    for line in results:
        if len(line.split(' ')) == 3:
            current_time, cw_value, timeout = line.split(' ')
        elif len(line.split(' ')) == 4:
            current_time, cw_value, _, timeout = line.split(' ')
        timeouts.append((float(current_time), float(timeout)))
        cw.append((float(current_time), float(cw_value)))
    return timeouts, cw


def get_reno_cw(cw_results):
    cw = []
    for line in cw_results:
        current_time, cw_value, rtt = line.split(' ')
        cw.append((float(current_time), float(cw_value)))
    return cw


def get_reno_rto(rto_results):
    cw = []
    for line in rto_results:
        current_time, rto = line.split(' ')
        cw.append((float(current_time), float(rto)))
    return cw


def load_tcp793(agent):
    computed_results = load_file(utils.get_agent_computed_cw_and_timeouts(agent))
    ns_results = load_file(utils.get_agent_ns_cw_and_timeouts(agent))

    # Obtain timeouts and congestion window values
    computed_timeouts, computed_cw = get_timeouts_and_cw(computed_results)
    ns_timeouts, ns_cw = get_timeouts_and_cw(ns_results)

    return computed_timeouts, computed_cw, ns_timeouts, ns_cw


def load_reno(agent):
    computed_results = load_file(utils.get_agent_computed_cw_and_timeouts(agent))
    ns_cw_results = load_file(utils.get_agent_ns_cw(agent))
    ns_rto_results = load_file(utils.get_agent_ns_rto(agent))

    # Obtain timeouts and congestion window values
    computed_timeouts, computed_cw = get_timeouts_and_cw(computed_results)
    ns_timeouts, ns_cw = get_reno_rto(ns_rto_results), get_reno_cw(ns_cw_results)

    return computed_timeouts, computed_cw, ns_timeouts, ns_cw


def plot_data(agent, computed_timeouts, ns_timeouts, computed_cw, ns_cw):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # Plot timeouts
    computed_times, computed_timeouts = zip(*computed_timeouts)
    ns_times, ns_timeouts = zip(*ns_timeouts)
    ax1.plot(ns_times, ns_timeouts, label="NS")
    ax1.plot(computed_times, computed_timeouts, label="Computed", color="red")
    ax1.set_ylabel("Timeout")
    ax1.legend()

    # Plot congestion window
    computed_times, computed_cw = zip(*computed_cw)
    ns_times, ns_cw = zip(*ns_cw)
    ax2.plot(ns_times, ns_cw, label="NS")
    ax2.plot(computed_times, computed_cw, label="Computed", color="red")
    ax2.set_ylabel("Congestion Window")
    ax2.set_xlabel("Time")
    ax2.legend()

    fig.suptitle("Agent: " + agent)
    plt.show()


def show_agent_simulation_results(agent):
    if agent == "tcp_rfc793":
        computed_timeouts, computed_cw, ns_timeouts, ns_cw = load_tcp793(agent)
    elif agent == "reno":
        computed_timeouts, computed_cw, ns_timeouts, ns_cw = load_reno(agent)
    else:
        raise ValueError(f"Agent {agent} not supported")

    plot_data(agent, computed_timeouts, ns_timeouts, computed_cw, ns_cw)
