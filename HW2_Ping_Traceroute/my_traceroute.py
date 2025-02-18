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
    parser.add_argument("-n", help="Print hop addresses numerically only",
                        action='store_true')
    parser.add_argument("-q", help="Number of probes per TTL",
                        type=int,
                        default=1)
    parser.add_argument("-S", help="Summary of how many probes "
                                   "unanswered for each hop",
                        action='store_true')
    return parser

def form_pkt():
    ip_layer = IP(dst="google.com")
    icmp_layer = ICMP()
    pkt = ip_layer / icmp_layer
    return pkt

def main():
    parser = setup_parser()
    args = parser.parse_args()
    line_break = "*" * 50

    pkt = form_pkt()
    ttl = 30
    timeout = 20
    flag = False
    probe_addresses = []
    failed_probes = []
    for i in range(1,ttl):
        pkt['IP'].ttl = i

        print(line_break)
        print("TTL set to ", i)

        probe_addr = set()
        ans, unans = srloop(pkt,timeout=timeout, verbose=0, count=args.q)
        if ans is not None:
            probe_num = 1
            for s, r in ans:
                print("Probe ", probe_num)
                print("Received: ", r.sprintf("{ICMP:%ICMP.type%} at %IP.src%"))
                probe_num += 1
                probe_addr.add(r['IP'].src)
                if s['IP'].dst == r['IP'].src:
                    print("Arrived at destination\n")
                    flag = True
        probe_addresses.append(probe_addr)
        failed_probes.append(len(unans))
        if flag:
            break

    if args.n or args.S:
        index = 0
        while index < len(probe_addresses):
            index += 1
            print(line_break)
            print("Hop #", index)
            if args.n:
                for addr in probe_addresses[index-1]:
                    print(addr)
            if args.S:
                print("The amount of probes unanswered: ", failed_probes[index-1])

if __name__ == "__main__":
    main()