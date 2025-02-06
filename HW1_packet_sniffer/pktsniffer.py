import argparse
import os.path
from HW1_packet_sniffer import config
import pyshark


# This is the absolute path to the cap_packets folder
# This is needed due to a bug where optional arguments
# if added rendered the program incapable of finding
# the cap_packets folder, absolute path prevents this
cap_folder_name = config.cap_folder_name

def file_exists(file_path):
    """Checks if a file exists based on the file path provided

    :param file_path: String of the file path
    :type file_path: str
    :return: file_path with cap_folder_name prepended if valid,
             else raises ArgumentTypeError
    :rtype: str
    :meta public:
    """
    file_path = os.path.join(cap_folder_name, file_path)
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' does not exist")
    return file_path

def setup_parser():
    """Sets up the argument parser for the program

    :return: parser, an initialized ArgumentParser object
    :rtype: ArgumentParser
    """
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
    """Sets up mutually exclusive argument group for packet type filtering

    :param parser: ArgumentParser object to set up argument group
    :type parser: ArgumentParser
    :return: None: parser is modified in place
    :rtype: None
    """
    type_group = parser.add_argument_group("Type",
                                           "Mutually Exclusive "
                                           "types to filter packets by")
    target_type = type_group.add_mutually_exclusive_group()
    target_type.add_argument("-host",
                             help="Show packets using a specific host")
    target_type.add_argument("-port",
                             help="Show packets using a specific port")
    target_type.add_argument("-net",
                             help="Show packets using a specific net address")
    return

def setup_proto_args(parser):
    """Sets up mutually exclusive argument group for packet protocol filtering

    :param parser: ArgumentParser object to set up argument group
    :type parser: ArgumentParser
    :return: None: parser is modified in place
    :rtype: None
    """
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
    """verifies if packet abides by the type qualifier filter criteria

    :param args: ArgumentParser object with parsed arguments
    :type args: ArgumentParser
    :param pkt: Pyshark packet to verify
    :type pkt: Pyshark Packet
    :return: pkt if verified, else None
    :rtype: Pyshark Packet or None
    """
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
    """verifies if packet abides by the proto qualifier filter criteria

    :param args: ArgumentParser object with parsed arguments
    :type args: ArgumentParser
    :param pkt: Pyshark packet to verify
    :type pkt: Pyshark Packet
    :return: pkt if verified, else None
    :rtype: Pyshark Packet or None
    """
    if args.ip is not None:
        return pkt
    elif args.tcp is not None:
        if pkt.transport_layer == "TCP":
            return pkt
        else:
            return None
    elif args.udp is not None:
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

def main():
    parser = setup_parser()
    args = parser.parse_args()
    cap_file = pyshark.FileCapture(input_file=args.file_name)
    line_break = "*"*100
    pkt_num = 1
    total_pkts_iterated = 0
    for pkt in cap_file:
        total_pkts_iterated += 1
        if len(pkt.layers) > 3 and (filter_pkt_proto(args,pkt) and
                filter_pkt_type(args,pkt)):
            print(line_break,"\nPacket Number: ", pkt_num)
            print(pkt[0])
            print(pkt[1])
            print(pkt[2])
        else:
            continue
        if args.c is not None and pkt_num >= args.c:
            break

        pkt_num += 1
    print("Iterated over ",total_pkts_iterated, " packets")



if __name__ == "__main__":
    main()
