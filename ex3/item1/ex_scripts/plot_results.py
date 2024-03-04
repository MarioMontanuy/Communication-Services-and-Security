import matplotlib.pyplot as plt
import utils


def load_results(computed_results_file, ns_results_file):
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
    plt.plot(computed_times, computed_timeouts, label="Computed", color="red")
    plt.xlabel("Time")
    plt.ylabel("Timeout")
    plt.title("Timeouts")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    args = utils.parse_args()
    computed_results, ns_results = load_results(utils.get_agent_computed_cw_and_timeouts(args.agent), utils.get_agent_ns_cw_and_timeouts(args.agent))

    # Obtain timeouts and congestion window values
    computed_timeouts, computed_cw = get_timeouts_and_cw(computed_results)
    ns_timeouts, ns_cw = get_timeouts_and_cw(ns_results)

    # Plot timeouts
    plot_timeouts(computed_timeouts, ns_timeouts)
