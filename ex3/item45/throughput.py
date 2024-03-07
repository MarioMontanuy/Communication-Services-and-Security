import sys

# type: python throughput.py <trace file> <required node> <granularity>   >    output file

infile = sys.argv[1]
tonode = sys.argv[2]

sum_bytes = 0
pck_list = []
try:
    with open(infile, 'r') as data:
        for line in data:
            x = line.split()
            if x[0] == 'r':
                if x[3] == tonode:
                    if x[4] == 'tcp':
                        if (pck_list.__contains__(x[10]) == False):
                            pck_list.append(x[10])
                            sum_bytes += int(x[5])
        print("Total throughput: " + str(sum_bytes))
        print("Average throughput per second: " + str(sum_bytes // 200))        
        print("Number of packets: " + str(len(pck_list)))
except FileNotFoundError:
    print(f"Can't open {infile}")

