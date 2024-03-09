import os, sys
sys.path.append(os.getcwd())

from agents.tcp_rfc793_agent import TCPAgent
from agents.tcp_reno_agent import TCPRenoAgent
from show_simulation_results import show_agent_simulation_results
from ex3.item1 import utils

def run_agent(agent, debug_mode=False):
    if agent == "tcp_rfc793":
        agent = TCPAgent("ex3/item1/ns_simulations/rfc793/sor.tcp_rfc_ss", debug=debug_mode)
    elif agent == "reno":
        agent = TCPRenoAgent("ex3/item1/ns_simulations/reno/sor.tcp_reno_ss", debug=debug_mode)
    else:
        raise ValueError(f"Agent {agent} not supported")
    
    agent.compute_timeout_and_cw()
    agent.write_results()

if __name__ == "__main__":
    args = utils.parse_args()
    debug_mode = False
    if args.d:
        debug_mode = True
    run_agent(args.agent, debug_mode)
    if not args.d:
        show_agent_simulation_results(args.agent)