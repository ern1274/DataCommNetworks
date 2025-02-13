import argparse
from scapy.all import *

def setup_parser():
    """Sets up the argument parser for the traceroute program

    :return: parser, an initialized ArgumentParser object
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Open Packet Capture File, "
                                                 "filter packets and Display"
                                                 " Packet Headers")
    parser.add_argument("-n", help="Print hop addresses numerically only")
    parser.add_argument("-q", help="Number of probes per TTL",
                        type=int)
    parser.add_argument("-S", help="Summary of how many probes "
                                   "unanswered for each hop")
    return parser

def form_pkt(args):
    ip_layer = IP(dst="google.com")
    icmp_layer = ICMP()
    pkt = ip_layer / icmp_layer
    return pkt

def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)
    pkt = form_pkt(args)
    ttl = 30
    for i in range(1,ttl):
        pkt['IP'].ttl = i
        ans, unans = sr(pkt,timeout=5, verbose=1)
        if ans is None:
            print("No Response.....")
        else:
            for s, r in ans:
                print("Send: ", s)
                print("Received: ", r)


if __name__ == "__main__":
    main()