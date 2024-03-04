from argparse import ArgumentParser
import utils

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

    return rtt_estimated, deviation, max(timeout, 0.2)

def timeout_and_cw_computation(trace, CWMAX=10):
    # Result
    timeouts = []
    
    # Jacobson/Karels algorithm variables
    rtt_estimated = None
    deviation = None

    # Auxiliary variables
    timeout = 3
    rtt_active = 0
    rtt_seq = -1
    rtt_begin_time = 0

    # Slow start congestion window
    cwini = 1.0
    cwnd = cwini
    cmax = CWMAX
    lost_segments = []
    # Save highest sent sequence number
    highest_seq_sent = -1

    # TODO: borrar rtt
    rtt_timer = -1
    timeout_recovery = False

    # Process tracefile
    for line in trace:
        event_type, current_time, source, destination, segment_type = line.split(' ')[:5]
        num_seq = line.split(' ')[-2]
        current_time = float(line.split(' ')[1])
        if event_type == '-' and segment_type == 'tcp' and source == '1' and destination == '2':
            # print("Packet sent", num_seq)
            highest_seq_sent = max(highest_seq_sent, int(num_seq))
            # Start RTT timer
            # if int(rtt_seq) >= int(highest_seq_sent) and rtt_active == 0:
            if rtt_active == 0:
                # if timeout_recovery:
                #     print("Sequence number", rtt_seq, "is in timeout recovery with highest sequence number", highest_seq_sent)
                if int(num_seq) >= int(highest_seq_sent):
                    rtt_active = 1
                    rtt_seq = num_seq
                    rtt_begin_time = current_time
                    timeout_recovery = False
                # else:
                #     rtt_active = 1
                #     rtt_seq = num_seq
                #     rtt_begin_time = current_time
                #     timeout_recovery = False

        if event_type == 'r' and segment_type == 'ack' and source == '2' and destination == '1':
            if num_seq == rtt_seq and rtt_active == 1:
                # Compute RTT and timeout applying Jacobson/Karels algorithm
                rtt_timer = current_time - rtt_begin_time
                rtt_estimated, deviation, timeout = jacobson_karels_algorithm(rtt_timer, rtt_estimated, deviation)
                # Stop RTT timer
                rtt_active = 0
                timeouts.append((current_time, cwnd, rtt_timer, timeout))
            # if num_seq not in acked_segments:
                # acked_segments.append(num_seq)
            # Update congestion window
            if cwnd < cmax:
                # exponential increase
                cwnd += 1
            else:
                # linear increase
                cwnd += 1/cwnd
                cmax = min(cwnd, CWMAX)


        if (current_time - rtt_begin_time) > timeout:
            # Timeout occurred
            rtt_active = 0
            timeout_recovery = True
            if rtt_seq not in lost_segments:
                cwnd = cwini
                cmax = int(max(cwini, cmax/2))
                lost_segments.append(rtt_seq)
            # print(f"Timeout occured at time {current_time} with sequence number {rtt_seq}")
            
        
        # Add line in result
        # timeouts.append((current_time, cwnd, rtt_timer, timeout))

    return timeouts
            
def write_results(timeouts):
    with open("timeouts.tcp_rfc793", "w") as file:
        for now, cw, rtt, timeout in timeouts:
            file.write(f"{now} {cw} {rtt} {timeout}\n")
        

if __name__ == "__main__":
    args = utils.parse_args()
    trace = read_trace_file(utils.get_agent_ns_trace(args.agent))
    timeouts = timeout_and_cw_computation(trace)
    write_results(timeouts)

