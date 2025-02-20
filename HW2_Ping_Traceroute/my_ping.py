import argparse
import time
from scapy.layers.inet import IP, ICMP
from scapy.packet import Padding
from scapy.sendrecv import srloop


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

def form_args(args, start_time):
    """Forms packet for ping program by using raw sockets

        :param args: ArgumentParser object with parsed arguments
        :type args: ArgumentParser
        :param start_time: Time object meant to represent start of ping process
        :type start_time: float
        :return: sr_args, kwargs for srloop() in main function
        :rtype: Dictionary
    """
    sr_args = {'verbose': 2, 'inter': args.i}
    if args.t is not None:
        sr_args['stop_filter'] = lambda p: time.time() - start_time > args.t
        sr_args['timeout'] = args.t
    if args.c is not None:
        sr_args['count'] = args.c
    return sr_args

def form_pkt(args):
    """Forms packet for ping program by using raw sockets

        :param args: ArgumentParser object with parsed arguments
        :type args: ArgumentParser
        :return: pkt, a crafted packet using scapy raw sockets
        :rtype: scapy.layers.inet.IP / scapy.layers.inet.ICMP / scapy.packet.Padding
    """
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

    pkt = form_pkt(args)
    start_time = time.time()
    sr_args = form_args(args, start_time)
    start_time = time.time()
    srloop(pkt,**sr_args)

if __name__ == "__main__":
    main()