import matplotlib.pyplot as plt
from argparse import ArgumentParser

agent_config = {
    "tcp_rfc793": {
        "computed_results": "timeouts.tcp_rfc793",
        "ns_results": "../ns_simulations/rfc793/cw.tcp_rfc_ss",
    }
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("agent", choices=agent_config.keys(), default="tcp_rfc793", nargs='?', help="Agent to plot results")
    return parser.parse_args()

def load_results(agent):
    computed_results_file = agent_config[agent]["computed_results"]
    ns_results_file = agent_config[agent]["ns_results"]
    with open(computed_results_file, "r") as file, open(ns_results_file, "r") as ns_file:
        computed_results = file.readlines()
        ns_results = ns_file.readlines()
    return computed_results, ns_results

def get_timeouts_and_cw(results):
    timeouts = []
    cw = []
    for line in results:
        current_time, cw_value, rtt_timer, timeout = line.split(' ')
        timeouts.append((float(current_time), float(timeout)))
        cw.append((float(current_time), float(cw_value)))
    return timeouts, cw

def plot_timeouts(computed_timeouts, ns_timeouts):
    computed_times, computed_timeouts = zip(*computed_timeouts)
    ns_times, ns_timeouts = zip(*ns_timeouts)

    # Plot timeouts using matplotlib
    plt.plot(ns_times, ns_timeouts, label="NS")
    plt.scatter(computed_times, computed_timeouts, label="Computed", color="red")
    plt.xlabel("Time")
    plt.ylabel("Timeout")
    plt.title("Timeouts")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    args = parse_args()
    computed_results, ns_results = load_results(args.agent)

    # Obtain timeouts and congestion window values
    computed_timeouts, computed_cw = get_timeouts_and_cw(computed_results)
    ns_timeouts, ns_cw = get_timeouts_and_cw(ns_results)

    # Plot timeouts
    plot_timeouts(computed_timeouts, ns_timeouts)
