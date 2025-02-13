import argparse

import scapy.all
from scapy.all import *

def setup_parser():
    """Sets up the argument parser for the ping program

    :return: parser, an initialized ArgumentParser object
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Open Packet Capture File, "
                                                 "filter packets and Display"
                                                 " Packet Headers")
    parser.add_argument("-c", help="Number of packets to send/receive",
                        type=int)
    parser.add_argument("-i", help="The length of time in seconds to "
                                   "wait between sending packets",
                        default=1,
                        type=float)
    parser.add_argument("-s", help="Number of data bytes to send",
                        default=56,
                        type=int)
    parser.add_argument("-t", help="The length of timeout in seconds before "
                                        "ping exits program",
                        type=float)

    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)

    ip_layer = IP()
    icmp_layer = ICMP()
    padding = Padding()
    # 28 is default length of both ip and icmp layers
    if args.s - 28 > 0:
        padding.load = '\x00' * (args.s - 28)
    packet = ip_layer / icmp_layer / padding

    print(packet)
    print(len(packet))
    answer = sr1(packet)
    print(answer)

if __name__ == "__main__":
    main()