class JacobsonRTT:
    def __init__(self, delta1: float=1/8, delta2: float=1/4, mu: float=1, phi: float=4):
        self.delta1 = delta1
        self.delta2 = delta2
        self.mu = mu
        self.phi = phi
        self.rtt_estimated = None
        self.deviation = None

    def compute_rtt(self, rtt: float) -> float:
        if self.rtt_estimated is None:
            # Fist RTT
            self.rtt_estimated = rtt
            self.deviation = rtt / 2
        else:
            diff = rtt - self.rtt_estimated
            self.rtt_estimated = self.rtt_estimated + self.delta1 * diff
            self.deviation = self.deviation + self.delta2 * (abs(diff) - self.deviation)
        timeout = self.mu * self.rtt_estimated + self.phi * self.deviation

        return max(timeout, 0.2)