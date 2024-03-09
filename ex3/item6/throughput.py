import sys

# type: python throughput.py <trace file> 

infile = sys.argv[1]

sum_bytes = 0
pck_list = []
try:
    with open(infile, 'r') as data:
        for line in data:
            event_type, _, source, _, segment_type, paket_size,  num_seq = line.split(' ')[:5] + [int(line.split(' ')[5])] + [int(line.split(' ')[-2])]
            if event_type == '-' and source == '1' and segment_type == 'tcp':
                if num_seq not in pck_list:
                    pck_list.append(num_seq)
                    sum_bytes += int(line.split(' ')[5])
        print("Total throughput: " + str(sum_bytes) + " bytes")
        print("Average throughput per second: " + str(sum_bytes // 200) + " bytes/sec")        
        print("Number of packets: " + str(len(pck_list)))
except FileNotFoundError:
    print(f"Can't open {infile}")

