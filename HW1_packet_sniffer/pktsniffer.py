from scapy.all import *
import argparse
import os.path
#from pathlib import Path
from HW1_packet_sniffer import config

# This is the absolute path to the cap_packets folder
# This is needed due to a bug where optional arguments
# if added rendered the program incapable of finding
# the cap_packets folder, absolute path prevents this
cap_folder_name = config.cap_folder_name

def file_exists(file_path):
    file_path = os.path.join(cap_folder_name, file_path)
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' does not exist")
    return file_path

def extract_headers(pkt):
    headers = []
    # Heavily depends on the packet having at least 3 layers/headers:
    # Ether header, IP header and Protocol header
    for i in range(2,-1, -1):
        header = pkt.getlayer(i)
        header.remove_payload()
        headers.insert(0,header.show(True))
    return headers

def main():

    parser = argparse.ArgumentParser(description="Open Packet Capture File, "
                                                 "filter packets and Display"
                                                 " Packet Headers")
    parser.add_argument("file_name",
                        help="Captured Packet File name",
                        type=file_exists)
    parser.add_argument("-c", help="Number of packets to show",
                        type=int)

    type_group = parser.add_argument_group("Type",
                              "Mutually Exclusive types to filter packets by")
    target_type = type_group.add_mutually_exclusive_group()
    # "Show packets using a specific host, port or net address"
    target_type.add_argument("-host",
                             help="Show packets using a specific host")
    target_type.add_argument("-port",
                             help="Show packets using a specific port")
    target_type.add_argument("-net",
                             help="Show packets using a specific net address")

    proto_group = parser.add_argument_group("Protocol",
                                           "Mutually Exclusive protocols "
                                           "to filter packets by")
    protocol = proto_group.add_mutually_exclusive_group()
    protocol.add_argument("-ip",
                          help= "IPV4 or IPV6 address")
    protocol.add_argument("-tcp")
    protocol.add_argument("-udp")
    protocol.add_argument("-icmp")

    args = parser.parse_args()

    #for arg in vars(args):
    #    print(arg, " " , getattr(args, arg))

    cap_file = sniff(offline=args.file_name)
    pkt_num = 1


    for pkt in cap_file:
        print(pkt_num)
        pkt_num += 1
        headers = extract_headers(pkt)
        ether_header= headers[0]
        ip_header = headers[1]
        protocol_header = headers[2]
        print("Ether Header: ")
        print(ether_header)
        print("IP Header: ")
        print(ip_header)
        print("Protocol: ")
        print(protocol_header)







main()