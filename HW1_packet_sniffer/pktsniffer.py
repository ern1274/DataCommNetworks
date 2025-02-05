import argparse
import os.path
from HW1_packet_sniffer import config
import pyshark


# This is the absolute path to the cap_packets folder
# This is needed due to a bug where optional arguments
# if added rendered the program incapable of finding
# the cap_packets folder, absolute path prevents this
cap_folder_name = config.cap_folder_name

malformed_pkts = 0

def file_exists(file_path):
    file_path = os.path.join(cap_folder_name, file_path)
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' does not exist")
    return file_path

def setup_parser():
    parser = argparse.ArgumentParser(description="Open Packet Capture File, "
                                                 "filter packets and Display"
                                                 " Packet Headers")
    parser.add_argument("file_name",
                        help="Captured Packet File name",
                        type=file_exists)
    parser.add_argument("-c", help="Number of packets to show",
                        type=int)
    setup_type_args(parser)
    setup_proto_args(parser)
    return parser

def setup_type_args(parser):
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
    return

def setup_proto_args(parser):
    proto_group = parser.add_argument_group("Protocol",
                                            "Mutually Exclusive protocols "
                                            "to filter packets by")
    protocol = proto_group.add_mutually_exclusive_group()
    protocol.add_argument("-ip", nargs='?', const="")
    protocol.add_argument("-tcp", nargs='?', const="")
    protocol.add_argument("-udp", nargs='?', const="")
    protocol.add_argument("-icmp", nargs='?', const="")
    return

def filter_pkt_type(args, pkt):
    try:
        layer = pkt[1]
        if args.host is not None:
            if layer.src == args.host or layer.dst == args.host:
                return pkt
            else:
                return None
        elif args.port is not None:
            if (pkt[2].srcport == args.port or
                    pkt[2].dstport == args.port):
                return pkt
            else:
                return None
        elif args.net is not None:
            if layer.src == args.net or layer.dst == args.net:
                return pkt
            else:
                return None
        return pkt
    except AttributeError:
        return None

def filter_pkt_proto(args, pkt):
    if args.ip is not None:
        return pkt
        #if pkt.transport_layer == "ip":
        #    return pkt
        #else:
        #    return None
    elif args.tcp is not None:
        if pkt.transport_layer == "TCP":
            return pkt
        else:
            return None
    elif args.udp is not None:
        #print("Here with: " , pkt.transport_layer)
        if pkt.transport_layer == "UDP":
            return pkt
        else:
            return None
    elif args.icmp is not None:
        if pkt.transport_layer == "ICMP":
            return pkt
        else:
            return None
    return pkt

def extract_eth_header(header):
    #print(header.field_names)
    line = ""
    line += "Destination: " + header.dst + "\n"
    line += "Source: " + header.src + "\n"
    line += "Ethertype: " + header.type + "\n"
    return line

def extract_ip_header(header):
    print(header.field_names)
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
    parser = setup_parser()
    args = parser.parse_args()
    cap_file = pyshark.FileCapture(input_file=args.file_name)
    #print(cap_file)
    line_break = "*"*100
    pkt_num = 1
    total_pkts_iterated = 0
    for pkt in cap_file:
        total_pkts_iterated += 1
        if len(pkt.layers) > 3 and (filter_pkt_proto(args,pkt) and
                filter_pkt_type(args,pkt)):
            print(line_break,"\nPacket Number: ", pkt_num)
            #print(pkt.pretty_print())
            print(pkt[0])
            print(pkt[1])
            print(pkt[2])
        else:
            continue
        if args.c is not None and pkt_num >= args.c:
            break

        pkt_num += 1
    print(total_pkts_iterated)







main()