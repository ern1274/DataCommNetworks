import argparse
import time
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

def form_pkt(args):
    ip_layer = IP()
    icmp_layer = ICMP()
    padding = Padding()
    if args.s - 28 > 0:
        padding.load = '\x00' * (args.s - 28)
    pkt = ip_layer / icmp_layer / padding
    return pkt

def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)

    pkt = form_pkt(args)
    print(pkt)

    sr_args = {'verbose': 2, 'inter': args.i}
    if args.t is not None:
        sr_args['stop_filter'] = lambda p: time.time() - start_time > args.t
        sr_args['timeout'] = args.t
    if args.c is not None:
        sr_args['count'] = args.c

    start_time = time.time()
    srloop(pkt,**sr_args)

if __name__ == "__main__":
    main()