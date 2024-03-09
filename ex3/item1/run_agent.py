from agents.tcp_rfc793_agent import TCPAgent

agent = TCPAgent("ns_simulations/rfc793/sor.tcp_rfc_ss")
agent.compute_timeout_and_cw()
agent.write_results()