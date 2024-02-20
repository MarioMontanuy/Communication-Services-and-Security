import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bandwith', type=str, help='Bandwith for each flow (as a percentage)', required=True)
parser.add_argument('-f', '--file', type=str, help='Path to the config file', required=True)
args = parser.parse_args()


def read_file():
    with open(args.file) as file:
        lines = [line.rstrip().split() for line in file]
    return lines

def main():
    bandwith = args.bandwith.split(',')
    print(bandwith)
    if sum(map(int, bandwith)) != 100:
        print("The sum of the bandwidth is not 100%")
        exit()       
    file_data = read_file()
    print(file_data)

if __name__ == "__main__":
    main()