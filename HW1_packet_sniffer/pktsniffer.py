from scapy.all import *
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP

cap_file_name = "cap_packets/pkt1.pcapng"

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
    cap_file = rdpcap(cap_file_name)

    i = 1
    for pkt in cap_file:
        print(i)
        i += 1
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