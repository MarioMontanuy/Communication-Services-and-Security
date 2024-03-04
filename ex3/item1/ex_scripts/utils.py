from argparse import ArgumentParser


agent_config = {
    "tcp_rfc793": {
        "trace_file": "../ns_simulations/rfc793/sor.tcp_rfc_ss",
        "computed_results": "timeouts.tcp_rfc793",
        "ns_results": "../ns_simulations/rfc793/cw.tcp_rfc_ss",
    }
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("agent", choices=agent_config.keys(), default="tcp_rfc793", nargs='?', help="Agent to plot results")
    return parser.parse_args()

def get_agent_ns_trace(agent):
    return agent_config[agent]["trace_file"]

def get_agent_ns_cw_and_timeouts(agent):
    return agent_config[agent]["ns_results"]

def get_agent_computed_cw_and_timeouts(agent):
    return agent_config[agent]["computed_results"]
