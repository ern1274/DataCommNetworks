from scapy.all import *
import argparse

cap_folder_name = "cap_packets/"

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
                        help="Captured Packet File name")
    parser.add_argument("-host",
                        help="To show packets from a specific host")

    parser.add_argument("-port",
                        help="To show packets from a specific port")

    parser.add_argument("-ip",
                        help="To show packets from a specific IP address")

    parser.add_argument("-net",
                        help="To show packets with destination and "
                             "source IP address")

    parser.add_argument("-c", help="Number of packets to show")

    parser.add_argument("-protocol",
                        help= "Show packets using a specific protocol",
                        choices=['tcp','udp','icmp'])

    args = parser.parse_args()


    cap_file_name = cap_folder_name + args.file_name
    cap_file = sniff(offline=cap_file_name)
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