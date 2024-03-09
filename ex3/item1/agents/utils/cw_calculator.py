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
    
    
class RenoCWCalculator:
    def __init__(self, CWMAX: int):
        self.cwnd = CWINI
        self.cmax = CWMAX
        self.CWMAX = CWMAX
        self.acked_segments = []
        self.lost_segments = []
        self.duplicated_segments = []
        
        # reno specific
        self.fast_recovery_sequence = -1
        self.fast_recovery_phase = False
        
    def compute_cw(self, num_seq: int, timeout: bool, duplicated: bool = False, fast_recovery_sequence: int = -1):
        if timeout:
            self.fast_recovery_phase = False
            if num_seq not in self.lost_segments:
                self.lost_segments.append(num_seq)
                self.cwnd = CWINI
                self.cmax = int(max(CWINI, self.cmax/2))
                self.acked_segments = []
            else:
                # Do nothing, segment already lost 
                pass
        elif duplicated and not self.fast_recovery_phase:
            self.cwnd = min(self.cwnd/2, self.CWMAX/2)
            self.cmax = int(max(CWINI, self.cmax/2))
            self.fast_recovery_phase = True
            self.fast_recovery_sequence = fast_recovery_sequence
            self.acked_segments = []
            self.duplicated_segments.append(num_seq)
        else:
            if num_seq >= self.fast_recovery_sequence:
                self.fast_recovery_phase = False
            if num_seq not in self.acked_segments:
                self.acked_segments.append(num_seq)
                if not num_seq in self.duplicated_segments:
                    if self.cwnd < self.cmax and not self.fast_recovery_phase:
                        self.cwnd += 1
                    else:
                        self.cwnd += 1/self.cwnd
                        self.cmax = min(self.cwnd, self.CWMAX)
                    
    def is_already_acked(self, num_seq: int):
        return num_seq in self.acked_segments
        
    