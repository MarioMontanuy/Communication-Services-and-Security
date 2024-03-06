import matplotlib.pyplot as plt
import utils

def load_file(file):
    with open(file, "r") as file:
        return file.readlines()

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

def plot_cw(computed_cw, ns_cw):
    computed_times, computed_cw = zip(*computed_cw)
    ns_times, ns_cw = zip(*ns_cw)

    # Plot timeouts using matplotlib
    plt.plot(ns_times, ns_cw, label="NS")
    plt.plot(computed_times, computed_cw, label="Computed", color="red")
    plt.xlabel("Time")
    plt.ylabel("Congestion Window")
    plt.title("Congestion Window")
    plt.legend()
    plt.show()

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


if __name__ == "__main__":
    args = utils.parse_args()
    if args.agent == "tcp_rfc793":
        computed_timeouts, computed_cw, ns_timeouts, ns_cw = load_tcp793(args.agent)
    elif args.agent == "reno":
        computed_timeouts, computed_cw, ns_timeouts, ns_cw = load_reno(args.agent)
    else:
        raise Exception("Agent not supported")
    

    # Plot timeouts
    plot_timeouts(computed_timeouts, ns_timeouts)

    # Plot congestion window
    plot_cw(computed_cw, ns_cw)
