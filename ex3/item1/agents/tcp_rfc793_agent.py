from agents.utils import read_trace_file, is_segment_sent_from_tcp_agent, is_segment_acknowledged_from_tcp_agent
from agents.utils.jacobson_rtt import JacobsonRTT
from agents.utils.cw_calculator import CWCalculator


class TCPAgent:
    def __init__(self, trace_file: str, CWMAX: int=10, rtt_algorithm: str = "jacobson_rtt"):
        self.trace = read_trace_file(trace_file)
        self.cw_calculator = CWCalculator(CWMAX)
        
        # Load RTT algorithm
        if rtt_algorithm == "jacobson_rtt":
            self.rtt_algorithm = JacobsonRTT()
        else:
            raise ValueError(f"RTT algorithm {rtt_algorithm} not supported")
        
        # Default values
        self.timeout = 3
        self.timeout_timer = 3
        self.cwnd = 1
        self.tolerance = 0.02
        
        # Auxiliary variables
        self.rtt_active = 0
        self.rtt_seq = -1
        self.rtt_begin_time = 0
        self.sent_segments = []
        
        # Results
        self.results_file = "agent_results/results.tcp_rfc793"
        self.results = []
       
        
    def compute_timeout_and_cw(self):
        for line in self.trace:
            event_type, current_time, source, destination, segment_type, num_seq = [line.split(' ')[0]] + [float(line.split(' ')[1])] + line.split(' ')[2:5] + [int(line.split(' ')[-2])]
            
            # Segment sent from TCP agent
            if is_segment_sent_from_tcp_agent(event_type, segment_type, source, destination):
                self.process_sent_segment(num_seq, current_time)
                    
            # Segment acknowledged from TCP agent
            if is_segment_acknowledged_from_tcp_agent(event_type, segment_type, source, destination):
                self.process_acked_segment(num_seq, current_time)
                
            # Timeout occurred
            if self.is_timeout(current_time):
                self.process_timeout()
                
            # Add line in result
            self.results.append((current_time, self.cw_calculator.cwnd, self.timeout))
            
    
    # METHODS TO PROCESS SEGMENTS
    def process_sent_segment(self, num_seq: int, current_time: float):
        # new segment is sent and rtt_active is 0
        if self.rtt_active == 0 and num_seq not in self.sent_segments:
            self.rtt_active = 1
            self.rtt_seq = num_seq
            self.rtt_begin_time = current_time
        # add to sent segments list
        self.sent_segments.append(int(num_seq))   
        
    def process_acked_segment(self, num_seq: int, current_time: float):
        if num_seq == self.rtt_seq and self.rtt_active == 1:
            # Compute RTT and timeout applying Jacobson/Karels algorithm
            rtt = current_time - self.rtt_begin_time
            self.update_timeout(rtt)
            # Stop RTT timer
            self.rtt_active = 0

        # Update congestion window
        if not self.is_acked_segment(num_seq):
            self.restart_timeout_timer(current_time)
            self.update_cw(num_seq, False)    
                
    def process_timeout(self):
        self.rtt_active = 0
        self.update_cw(self.rtt_seq, True)
        
        
    # AUXILIARY METHODS
    def restart_timeout_timer(self, current_time: float):
        self.timeout_timer = current_time
        
    def update_timeout(self, rtt):
        self.timeout = self.rtt_algorithm.compute_rtt(rtt)
        
    def update_cw(self, num_seq: int, timeout: bool):
        self.cw_calculator.compute_cw(num_seq, timeout)
        
    def is_acked_segment(self, num_seq: int):
        return self.cw_calculator.is_already_acked(num_seq)
        
    def is_timeout(self, current_time: float):
        if current_time == 125.792555:
            print(self.timeout_timer)
            print(f"Timeout: {current_time - self.timeout_timer} > {self.timeout + self.tolerance}")
        return (current_time - self.timeout_timer) > (self.timeout + self.tolerance)
    
    def write_results(self):
        with open(self.results_file, "w") as file:
            for now, cw, timeout in self.results:
                file.write(f"{now} {cw} {timeout}\n")
            
            
        
    



