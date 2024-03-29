from argparse import ArgumentParser


agent_config = {
    "tcp_rfc793": {
        "trace_file": "ex3/item1/ns_simulations/rfc793/sor.tcp_rfc_ss",
        "computed_results": "ex3/item1/agent_results/results.tcp_rfc793",
        "ns_results": "ex3/item1/ns_simulations/rfc793/cw.tcp_rfc_ss",
    },
    "reno": { 
        "trace_file": "ex3/item1/ns_simulations/reno/sor.tcp_reno_ss",
        "computed_results": "ex3/item1/agent_results/results.tcp_reno",
        "ns_cw_results": "ex3/item1/ns_simulations/reno/cw.tcp_reno_ss",
        "ns_rto_results": "ex3/item1/ns_simulations/reno/rto.tcp_reno_ss",
    },
    "reno+red+wait_false": {
        "ns_cw_results": "ex3/item6/wait_false/cw.tcp_Reno_item6_ss",
    },
    "reno+red+wait_true": {
        "ns_cw_results": "ex3/item6/wait_true/cw.tcp_Reno_item6_ss",
    },
    "newreno": {
        "ns_cw_results": ".ex3/item4/newreno/cw.tcp_Newreno_ss",
    },
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("agent", choices=agent_config.keys(), default="tcp_rfc793", nargs='?', help="Agent to plot results")
    parser.add_argument("--d", action="store_true", help="Debug mode")
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