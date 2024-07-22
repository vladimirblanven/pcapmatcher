import argparse
import os
from scapy.all import rdpcap
from collections import namedtuple

PacketInfo = namedtuple('PacketInfo', ['timestamp', 'packet'])

def read_pcap(file):
    try:
        packets = rdpcap(file)
        return [PacketInfo(packet.time, packet) for packet in packets]
    except FileNotFoundError:
        print(f"Error: File {file} not found.")
        return None
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return None

def find_matching_intervals(packets_a, packets_b, min_match_length):
    intervals = []
    i, j = 0, 0

    while i < len(packets_a) and j < len(packets_b):
        if packets_a[i].packet == packets_b[j].packet:
            start_a, start_b = i, j
            match_length = 0

            while i < len(packets_a) and j < len(packets_b) and packets_a[i].packet == packets_b[j].packet:
                match_length += 1
                i += 1
                j += 1

            if match_length >= min_match_length:
                intervals.append((start_a, start_b, match_length))

        i += 1
        j += 1

    return intervals

def print_interval_info(intervals, packets_a, packets_b, interval_numbers, file_a_name, file_b_name):
    for interval_number in interval_numbers:
        if interval_number < len(intervals):
            start_a, start_b, match_length = intervals[interval_number]
            print(f"Interval {interval_number + 1}:")
            print(f"  Number of matching packets: {match_length}")
            print(f"  First matching packet in {file_a_name}: Packet #{start_a + 1}, Timestamp: {packets_a[start_a].timestamp}")
            print(f"  First matching packet in {file_b_name}: Packet #{start_b + 1}, Timestamp: {packets_b[start_b].timestamp}")
        else:
            print(f"Interval {interval_number + 1} not found.")

def main():
    parser = argparse.ArgumentParser(description="Find matching intervals in two pcap files.")
    parser.add_argument("file_a", type=str, help="First pcap file")
    parser.add_argument("file_b", type=str, help="Second pcap file")
    parser.add_argument("--min-match-length", type=int, default=3, help="Minimum number of matching packets in an interval")
    parser.add_argument("--interval-numbers", type=int, nargs='+', default=[0], help="Interval numbers to display")

    args = parser.parse_args()

    if not os.path.isfile(args.file_a):
        print(f"Error: File {args.file_a} not found.")
        return

    if not os.path.isfile(args.file_b):
        print(f"Error: File {args.file_b} not found.")
        return

    packets_a = read_pcap(args.file_a)
    packets_b = read_pcap(args.file_b)

    if packets_a is None or packets_b is None:
        return

    intervals = find_matching_intervals(packets_a, packets_b, args.min_match_length)

    print(f"Total matching intervals: {len(intervals)}")
    print_interval_info(intervals, packets_a, packets_b, args.interval_numbers, args.file_a, args.file_b)

if __name__ == "__main__":
    main()