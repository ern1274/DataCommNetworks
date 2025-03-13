import socket
from HW3_RDT_Protocol.receiver_rdt import Receiver
from HW3_RDT_Protocol.sender_rdt import Sender


def make_packets(file_name):
    file = open(file_name, 'r')
    pkts = []
    file.close()
    return pkts

def send_file(file_name, ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender = Sender(soc, ip, port)
    sender.arrange_pkts(make_packets(file_name))
    sender.run_sender()
    print("Sent file")
    return

def receive_file(file_name, ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((ip, port))
    receiver = Receiver(soc)
    receiver.run_receiver()
    pkts = receiver.get_packets()
    new_file_name = file_name + '_recv.txt'
    file = open(new_file_name, 'w')
    # Write pkts to file
    file.close()
    return



