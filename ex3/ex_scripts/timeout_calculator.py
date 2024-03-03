from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("trace_file")
    return parser.parse_args()

def read_trace_file(trace_file):
    with open(trace_file, "r") as file:
        return file.readlines()
    
def jacobson_karels_algorithm(rtt: float, rtt_estimated: float, deviation: float, delta1: float=1/8, delta2: float=1/4, mu: float=1, phi: float=4):
    if rtt_estimated is None:
        # Fist RTT
        rtt_estimated = rtt
        deviation = rtt / 2
    else:
        diff = rtt - rtt_estimated
        rtt_estimated = rtt_estimated + delta1 * diff
        deviation = deviation + delta2 * (abs(diff) - deviation)
    timeout = mu * rtt_estimated + phi * deviation

    return rtt_estimated, deviation, timeout

def timeout_computation(trace):
    # Result
    timeouts = []
    
    # Jacobson/Karels algorithm variables
    rtt_estimated = None
    deviation = None

    # Auxiliary variables
    timeout = 3
    rtt_active = 0
    rtt_seq = None
    rtt_begin_time = 0

    # Process tracefile
    for line in trace:
        event_type, current_time, source, destination, segment_type = line.split(' ')[:5]
        num_seq = line.split(' ')[-2]
        current_time = float(line.split(' ')[1])
        if event_type == '-' and segment_type == 'tcp' and rtt_active == 0 and source == '1' and destination == '2':
            # print("Packet sent", line)
            # Start RTT timer
            rtt_active = 1
            rtt_seq = num_seq
            rtt_begin_time = current_time
        if event_type == 'r' and segment_type == 'ack' and rtt_active == 1 and num_seq == rtt_seq and source == '2' and destination == '1':
            # print("Packet acked", line)
            # Compute RTT and timeout applying Jacobson/Karels algorithm
            rtt_timer = current_time - rtt_begin_time
            rtt_estimated, deviation, timeout = jacobson_karels_algorithm(rtt_timer, rtt_estimated, deviation)
            timeouts.append((current_time, rtt_timer, timeout))
            # Stop RTT timer
            rtt_active = 0

        if (current_time - rtt_begin_time) >= (timeout - 0.01):
            # Timeout occurred
            rtt_active = 0
            print("Timeout occured")

    return timeouts
            
def write_results(timeouts):
    with open("timeouts.tcp_rfc793", "w") as file:
        for now, rtt, timeout in timeouts:
            file.write(f"{now} {rtt} {timeout}\n")
        

if __name__ == "__main__":
    args = parse_args()
    trace = read_trace_file(args.trace_file)
    timeouts = timeout_computation(trace)
    write_results(timeouts)

