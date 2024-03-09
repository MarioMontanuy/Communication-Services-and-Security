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
    sent_segments = []
    lost_segments = []
    acked_segments = []
    highest_seq_sent = -1

    # TODO: borrar rtt
    rtt_timer = -1
    timeout_timer_begin_time = 3

    # Process tracefile
    for line in trace:
        event_type, current_time, source, destination, segment_type = line.split(' ')[:5]
        num_seq = line.split(' ')[-2]
        current_time = float(line.split(' ')[1])
        if event_type == '-' and segment_type == 'tcp' and source == '1' and destination == '2':
            # print("Packet sent", num_seq)
            highest_seq_sent = max(highest_seq_sent, int(num_seq))
            
            # Start RTT timer
            if rtt_active == 0 and int(num_seq) not in sent_segments:
                print(f"Starting RTT timer for sequence number {num_seq}")

                rtt_active = 1
                rtt_seq = num_seq
                rtt_begin_time = current_time
            
            sent_segments.append(int(num_seq))

        if event_type == 'r' and segment_type == 'ack' and source == '2' and destination == '1':
            if num_seq == rtt_seq and rtt_active == 1:
                # Compute RTT and timeout applying Jacobson/Karels algorithm
                rtt_timer = current_time - rtt_begin_time
                rtt_estimated, deviation, timeout = jacobson_karels_algorithm(rtt_timer, rtt_estimated, deviation)
                # Stop RTT timer
                rtt_active = 0
                # timeouts.append((current_time, cwnd, rtt_timer, timeout))
            
            if int(num_seq) not in acked_segments:
                timeout_timer_begin_time = current_time
                acked_segments.append(int(num_seq))
                # Update congestion window
                if cwnd < cmax:
                    # exponential increase
                    cwnd += 1
                else:
                    # linear increase
                    cwnd += 1/cwnd
                    cmax = min(cwnd, CWMAX)


        if (current_time - timeout_timer_begin_time) > (timeout + 0.02):
            # Timeout occurred
            rtt_active = 0
            if rtt_seq not in lost_segments:
                cwnd = cwini
                cmax = int(max(cwini, cmax/2))
                lost_segments.append(rtt_seq)
                acked_segments = []
            # print(f"Timeout occured at time {current_time} with sequence number {rtt_seq}")
            
        
        # Add line in result
        timeouts.append((current_time, cwnd, rtt_timer, timeout))

    return timeouts

def timeout_and_cw_computation_reno(trace, CWMAX=10):
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
    sent_segments = []
    lost_segments = []
    acked_segments = []
    duplicated_segments = []
    last_acked = -1
    times_last_acked = 0

    # TODO: borrar rtt
    rtt_timer = -1
    timeout_timer_begin_time = 3

    # Reno
    fast_recovery_phase = False
    fast_recovery_segment = -1

    # Process tracefile
    for line in trace:
        event_type, current_time, source, destination, segment_type = line.split(' ')[:5]
        num_seq = line.split(' ')[-2]
        current_time = float(line.split(' ')[1])
        if event_type == '-' and segment_type == 'tcp' and source == '1' and destination == '2':           
            # Start RTT timer
            if rtt_active == 0 and int(num_seq) not in sent_segments:
                print(f"{current_time}: Packet sent {num_seq}")
                rtt_active = 1
                rtt_seq = num_seq
                rtt_begin_time = current_time
            
            sent_segments.append(int(num_seq))

        if event_type == 'r' and segment_type == 'ack' and source == '2' and destination == '1':
            if num_seq == rtt_seq and rtt_active == 1:
                print(f"{num_seq}")
                # Compute RTT and timeout applying Jacobson/Karels algorithm
                rtt_timer = current_time - rtt_begin_time
                rtt_estimated, deviation, timeout = jacobson_karels_algorithm(rtt_timer, rtt_estimated, deviation)
                # Stop RTT timer
                rtt_active = 0
                # timeouts.append((current_time, cwnd, rtt_timer, timeout))
            
            if int(num_seq) not in acked_segments:
                timeout_timer_begin_time = current_time
                acked_segments.append(int(num_seq))
                if int(num_seq) >= fast_recovery_segment:
                    fast_recovery_phase = False
                if int(num_seq) not in duplicated_segments:
                    # Update congestion window
                    if cwnd < cmax and not fast_recovery_phase:
                        # exponential increase
                        cwnd += 1
                    else:
                        # linear increase
                        cwnd += 1/cwnd
                        cmax = min(cwnd, CWMAX)

            # Reno
            if int(num_seq) != last_acked:
                last_acked = int(num_seq)
                times_last_acked = 1
            else:
                times_last_acked += 1


        if (current_time - timeout_timer_begin_time) > (timeout + 0.02):
            # Timeout occurred
            rtt_active = 0
            fast_recovery_phase = False
            if rtt_seq not in lost_segments:
                cwnd = cwini
                cmax = int(max(cwini, cmax/2))
                timeout = 2 * timeout
                lost_segments.append(rtt_seq)
                acked_segments = []
            print(f"{current_time}:Timeout occured with sequence number {rtt_seq}")
                
        if times_last_acked == 4 and not fast_recovery_phase:
            # print("Received 3rd duplicate ACK for sequence number", last_acked)
            # print("current RTT packet", rtt_seq)
            rtt_active = 0
            cwnd = min(cwnd/2, CWMAX/2)
            cmax = int(max(cwini, cmax/2))
            times_last_acked = 0
            fast_recovery_phase = True
            fast_recovery_segment = sent_segments[-1]
            acked_segments = []
            duplicated_segments.append(last_acked)
            timeout_timer_begin_time = current_time
            
        
        # Add line in result
        timeouts.append((current_time, cwnd, rtt_timer, timeout))

    return timeouts
            
def write_results(timeouts, agent):
    output_file = utils.get_agent_computed_cw_and_timeouts(agent=agent)
    with open(output_file, "w") as file:
        for now, cw, rtt, timeout in timeouts:
            file.write(f"{now} {cw} {rtt} {timeout}\n")
        

if __name__ == "__main__":
    args = utils.parse_args()
    trace = read_trace_file(utils.get_agent_ns_trace(args.agent))
    if args.agent == "tcp_rfc793":
        timeouts = timeout_and_cw_computation(trace)
    elif args.agent == "reno":
        timeouts = timeout_and_cw_computation_reno(trace)
    write_results(timeouts, args.agent)

