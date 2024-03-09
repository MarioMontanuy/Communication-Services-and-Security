
def read_trace_file(trace_file):
    with open(trace_file, "r") as file:
        return file.readlines()
    
def is_segment_sent_from_tcp_agent(event_type, segment_type, source, destination):
    return event_type == '-' and segment_type == 'tcp' and source == '1' and destination == '2'

def is_segment_acknowledged_from_tcp_agent(event_type, segment_type, source, destination):
    return event_type == 'r' and segment_type == 'ack' and source == '2' and destination == '1'