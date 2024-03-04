import argparse
from fractions import Fraction

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bandwith', type=str, help='Bandwith for each flow (as a percentage)', required=True)
parser.add_argument('-f', '--file', type=str, help='Path to the config file', required=True)
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

class Packet:
    def __init__(self, pck_id, flow_id ,arrival_time, size, f):
        self.pck_id = pck_id
        self.flow_id = flow_id
        self.arrival_time = arrival_time
        self.size = size
        self.f = f
    
    def get_flow_id(self):
        return self.flow_id

    def get_size(self):
        return float(self.size)

    def get_f(self):
        return float(self.f)

    def __str__(self):
        return f"Packet with id {self.pck_id} from flow {self.flow_id} with arrival time {self.arrival_time} and size {self.size} and f {self.f}"

def get_ratio(flow_percentage):
    flow_float = float(flow_percentage) / 100
    if (args.debug):
        print("Flow float: " + str(flow_float))
    ratio = Fraction(flow_float).limit_denominator()
    if (args.debug):
        print("Ratio : " + str(ratio.numerator) + " " + str(ratio.denominator))
    if(ratio.numerator != 1):
        new_denominator = ratio.denominator / ratio.numerator
        if (args.debug):
            print("New denominator: " + str(new_denominator))
        return new_denominator
    return ratio.denominator

def calculate_f_initial_packet(arrival_time, size, flow_percentage):
    if (args.debug):
        print("Arrival time: " + str(arrival_time) + " Size: " + str(size) + " Flow percentage: " + str(flow_percentage))
    f = float(arrival_time) + float(size) * get_ratio(flow_percentage)
    if (args.debug):
        print("F: " + str(f))
    return f

def calculate_f_next_packet(arrival_time, size, f, flow_percentage):
    if (args.debug):
        print("Arrival time: " + str(arrival_time) + " Size: " + str(size) + " F: " + str(f) + " Flow percentage: " + str(flow_percentage))
    f = max(float(f), float(arrival_time)) + float(size) * get_ratio(flow_percentage)
    if (args.debug):
        print("F: " + str(f))
    return f

    
def read_file():
    with open(args.file) as file:
        lines = [line.rstrip().split() for line in file]
    return lines

def get_next(queue):
    return min(queue, key=lambda x: x.f)


def wfq(bandwith, file_data):
    current_packet = Packet(0, 0, 0, 0, 0)
    pck_id = 0
    time = 0.0
    queue = [] 
    result = []
    for pck in file_data:
        pck_id += 1
        if (args.debug):
            print("-------------------")
            print("Packet: " + pck[0] + " " + pck[1] + " " + pck[2])
        # print("Current packet in transit: " + current_packet.__str__())
        # for item in queue:
        #     print(item.__str__())
        # Start
        if queue == []:
            if (args.debug):
                print("Queue is empty")
            packet = Packet(pck_id, pck[2], pck[0], pck[1], calculate_f_initial_packet(pck[0], pck[1], bandwith[int(pck[2]) - 1]))
            time = float(pck[0])
            queue.append(packet)
        else:
            if (args.debug):
                print("Queue is not empty")
            if queue[0].arrival_time == pck[0]:
                if (args.debug):
                    print("Same arrival time")
                packet = Packet(pck_id, pck[2], pck[0], pck[1], calculate_f_initial_packet(pck[0], pck[1], bandwith[int(pck[2]) - 1])) 
                queue.append(packet)
            else:
                if (args.debug):
                    print("Different arrival time")
                # current_packet = get_next(queue)
                # time += current_packet.get_size()
                # queue.remove(current_packet)
                # result.append(current_packet)
                
                # Next
                if(float(pck[0]) <= time):
                    if (args.debug):
                        print("Packet is less than time")
                    packet = Packet(pck_id, pck[2], pck[0], pck[1], calculate_f_next_packet(pck[0], pck[1], current_packet.f, bandwith[int(pck[2]) - 1]))
                    queue.append(packet)
                else:
                    if (args.debug):
                        print("Packet is greater than time")
                    # queue.remove(current_packet)
                    current_packet = get_next(queue)
                    time += current_packet.get_size()
                    queue.remove(current_packet)
                    result.append(current_packet)
                    if (args.debug):
                        print("time: " + str(time))
                        print("Current packet in transit: " + current_packet.__str__())
                    packet = Packet(pck_id, pck[2], pck[0], pck[1], calculate_f_next_packet(pck[0], pck[1], current_packet.f, bandwith[int(pck[2]) - 1]))
                    queue.append(packet)
    while queue != []:
        current_packet = get_next(queue)
        queue.remove(current_packet)
        result.append(current_packet)
    if (args.debug):
        print("Result length: " + str(len(result)))
    for item in result:
        print(item.__str__())

def main():
    bandwith = args.bandwith.split(',')
    if (args.debug):
        print("Bandwith: " + str(bandwith))
    if sum(map(int, bandwith)) != 100:
        if (args.debug):
            print("The sum of the bandwidth is not 100%")
        exit()       
    file_data = read_file()
    if (args.debug):
        print("Data: " + str(file_data))

    wfq(bandwith, file_data)

if __name__ == "__main__":
    main()
