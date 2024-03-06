from argparse import ArgumentParser


agent_config = {
    "tcp_rfc793": {
        "trace_file": "../ns_simulations/rfc793/sor.tcp_rfc_ss",
        "computed_results": "timeouts.tcp_rfc793",
        "ns_results": "../ns_simulations/rfc793/cw.tcp_rfc_ss",
    },
    "reno": { 
        "trace_file": "../ns_simulations/reno/sor.tcp_reno_ss",
        "computed_results": "timeouts.tcp_reno",
        "ns_cw_results": "../ns_simulations/reno/cw.tcp_reno_ss",
        "ns_rto_results": "../ns_simulations/reno/rto.tcp_reno_ss",
    }
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("agent", choices=agent_config.keys(), default="reno", nargs='?', help="Agent to plot results")
    return parser.parse_args()

def get_agent_ns_trace(agent):
    return agent_config[agent]["trace_file"]

def get_agent_ns_cw_and_timeouts(agent):
    return agent_config[agent]["ns_results"]

def get_agent_computed_cw_and_timeouts(agent):
    return agent_config[agent]["computed_results"]

def get_agent_ns_cw(agent):
    try:
        return agent_config[agent]["ns_cw_results"]
    except KeyError:
        raise Exception(f"Agent {agent} does not support ns_cw_results")

def get_agent_ns_rto(agent):
    try:
        return agent_config[agent]["ns_rto_results"]
    except KeyError:  
        raise Exception(f"Agent {agent} does not support ns_rto_results")