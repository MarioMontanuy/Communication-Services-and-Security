import sys

# type: python throughput.py <trace file> <required node> <granularity>   >    output file

infile = sys.argv[1]

sum_bytes = 0
pck_list = []
try:
    with open(infile, 'r') as data:
        for line in data:
            x = line.split()
            if x[0] == '-':
                if x[2] == '1':
                    if x[4] == 'tcp':
                        if (pck_list.__contains__(x[10]) == False):
                            pck_list.append(x[10])
                            sum_bytes += int(x[5])
        print("Total throughput: " + str(sum_bytes) + " bytes")
        print("Throughput per second: " + str(sum_bytes // 200) + " bytes/sec")        
        print("Total number of packets: " + str(len(pck_list)))
except FileNotFoundError:
    print(f"Can't open {infile}")

