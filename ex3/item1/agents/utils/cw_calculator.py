CWINI = 1.0

class CWCalculator:
    def __init__(self, CWMAX: int):
        self.cwnd = CWINI
        self.cmax = CWMAX
        self.CWMAX = CWMAX
        self.acked_segments = []
        self.lost_segments = []
        
    def compute_cw(self, num_seq: int, timeout: bool):
        if timeout:
            if num_seq not in self.lost_segments:
                self.lost_segments.append(num_seq)
                self.cwnd = CWINI
                self.cmax = int(max(CWINI, self.cmax/2))
                self.acked_segments = []
            else:
                # Do nothing, segment already lost 
                pass
        else:
            if num_seq not in self.acked_segments:
                self.acked_segments.append(num_seq)
                if self.cwnd < self.cmax:
                    self.cwnd += 1
                else:
                    self.cwnd += 1/self.cwnd
                    self.cmax = min(self.cwnd, self.CWMAX)
                    
    def is_already_acked(self, num_seq: int):
        return num_seq in self.acked_segments
        
    