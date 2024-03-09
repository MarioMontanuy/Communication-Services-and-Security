from agents.tcp_rfc793_agent import TCPAgent
from agents.tcp_reno_agent import TCPRenoAgent

agent = TCPAgent("ns_simulations/rfc793/sor.tcp_rfc_ss")
agent.compute_timeout_and_cw()
agent.write_results()

agent = TCPRenoAgent("ns_simulations/reno/sor.tcp_reno_ss")
agent.compute_timeout_and_cw()
agent.write_results()