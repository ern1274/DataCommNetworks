from scapy.all import *
import argparse
import os.path
from HW1_packet_sniffer import config
import pyshark
import libpcap
conf.use_pcap = True

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

def extract_eth_header(header):
    #print(header.field_names)
    line = ""
    line += "Destination: " + header.dst + "\n"
    line += "Source: " + header.src + "\n"
    line += "Ethertype: " + header.type + "\n"
    return line

def extract_ip_header(header):
    #print(header.field_names)
    line = ""
    line += "Version: " + header.version + "\n"
    line += "Header Length: " + header.hdr_len + "\n"
    line += "Type of Service: " + header.dsfield + "\n"
    line += "Total length: " + header.len + "\n"
    line += "Identification: " + header.id + "\n"
    line += "Flags: " + header.flags + "\n"
    line += "Fragment Offset: " + header.frag_offset + "\n"
    line += "Time to live: : " + header.ttl + "\n"
    line += "Protocol: " + header.proto + "\n"
    line += "Header Checksum: " + header.checksum + "\n"
    line += "Source IP: " + header.src + "\n"
    line += "Destination IP: " + header.dst + "\n"
    return line

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
                          help= "IPV4 or IPV6 address",
                          nargs='?',
                          const="")
    protocol.add_argument("-tcp",
                          nargs='?',
                          const="")
    protocol.add_argument("-udp",
                          nargs='?',
                          const="")
    protocol.add_argument("-icmp",
                          nargs='?',
                          const="")

    args = parser.parse_args()

    sniff_args = {'offline': args.file_name}
    if args.c is not None:
        sniff_args['count'] = args.c

    filter = ""
    and_flag = False
    for arg in vars(args):
        value = getattr(args, arg)
        if arg != 'file_name' and arg != 'c' and value is not None:
            if and_flag:
                filter += " and " + arg + " " + value
            else:
                filter += arg + " " + value
                and_flag = True
        print(arg, " " , value)

    sniff_args['filter'] = filter
    #cap_file = pyshark.FileCapture(input_file=args.file_name,)
    #print(cap_file)
    #cap_file = sniff(offline=args.file_name)
    cap_file = sniff(**sniff_args)
    pkt_num = 1

    for pkt in cap_file:
        print("Packet Number: ", pkt_num)
        ether_header = pkt.eth
        ip_header = pkt.ip
        protocol_header = pkt.transport_layer
        headers = extract_headers(pkt)
        ether_header= headers[0]
        ip_header = headers[1]
        protocol_header = headers[2]
        print(ether_header)
        print(ip_header)
        print(protocol_header)
        '''print(vars(pkt))
        ether_header = "Length: " + pkt.length + "\n" + extract_eth_header(ether_header)
        print("Ether Header: ")
        print(ether_header)
        ip_header = extract_ip_header(ip_header)
        print("IP Header: ")
        print(ip_header)
        print("Protocol: ")
        print(protocol_header)
        if args.c is not None and pkt_num >= args.c:
            break
        '''
        pkt_num += 1








main()