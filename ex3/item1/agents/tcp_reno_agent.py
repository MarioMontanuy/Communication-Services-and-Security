from agents.tcp_rfc793_agent import TCPAgent
from agents.utils.cw_calculator import RenoCWCalculator

class TCPRenoAgent(TCPAgent):
    def __init__(self, trace_file: str, CWMAX: int=10, rtt_algorithm: str = "jacobson_rtt"):
        super().__init__(trace_file, CWMAX, rtt_algorithm)
        self.cw_calculator = RenoCWCalculator(CWMAX)
        
        # Reno specific
        self.last_acked = -1
        self.times_last_acked = 0
        
        # Results
        self.results_file = "agent_results/results.tcp_reno"
        
    def process_acked_segment(self, num_seq: int, current_time: float):
        super().process_acked_segment(num_seq, current_time)
        # Look for duplicated acks
        if int(num_seq) != self.last_acked:
            self.last_acked = int(num_seq)
            self.times_last_acked = 1
        else:
            self.times_last_acked += 1
            
        if self.times_last_acked == 4 and not self.is_fast_recovery_phase():
            # Stop RTT timer
            self.rtt_active = 0
            self.restart_timeout_timer(current_time)
            # Update congestion window
            self.update_cw(self.last_acked, timeout=False, duplicated=True, fast_recovery_sequence=self.sent_segments[-1])
            self.times_last_acked = 0
            
    def update_cw(self, num_seq: int, timeout: bool, duplicated: bool = False, fast_recovery_sequence: int = -1):
        self.cw_calculator.compute_cw(num_seq, timeout, duplicated, fast_recovery_sequence=fast_recovery_sequence)
        
    def is_fast_recovery_phase(self):
        return self.cw_calculator.fast_recovery_phase
        
    def process_timeout(self):
        super().process_timeout()
        self.timeout = 2 * self.timeout