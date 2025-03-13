import random
import socket
import zlib
import sys
from multiprocessing import Process
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1, send, sniff

from HW3_RDT_Protocol.sender_rdt import Sender
from HW3_RDT_Protocol.receiver_rdt import Receiver



def run_sender(ip, port):
    print("Started Client")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender = Sender(soc, ip, port)
    print(sender.ip)
    print(sender.port)
    print(sender.base_seq)
    data = [i for i in range(15)]
    sender.arrange_pkts(data)
    sender.run_sender()


def run_receiver(ip, port):
    #print("Started Server")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((ip,port))
    receiver = Receiver(soc)
    print(receiver.packets)
    print(receiver.base_seq)
    print(receiver.max_seq)
    receiver.run_receiver()


def run_router(ip, sender_port, receiver_port):
    print('Started Router')
    router_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    router_soc.bind((ip, sender_port))
    while True:
        sender_data, sender_address = router_soc.recvfrom(4096)
        if random.randint(0,100) > 80:
            print("Lost packet from sender to receiver")
            continue
        router_soc.sendto(sender_data, (ip,receiver_port))
        # add chance of corruption but learn the checksum first
        receiver_data, receiver_address = router_soc.recvfrom(4096)
        if random.randint(0,100) > 80:
            print("Lost packet from receiver to sender")
            continue
        router_soc.sendto(receiver_data, sender_address)


    return

def test_with_router():
    ip = '127.0.0.1'
    sender_port = 5000
    receiver_port = 5001

    router = Process(target=run_router, args=[ip, sender_port, receiver_port])
    router.start()

    receiver = Process(target=run_receiver, args=[ip, receiver_port])
    receiver.start()

    sender = Process(target=run_sender, args=[ip, sender_port])
    sender.start()

def test():
    ip = '127.0.0.1'
    sender_port = 5000
    receiver_port = 5000

    receiver = Process(target=run_receiver, args=[ip, receiver_port])
    receiver.start()

    sender = Process(target=run_sender, args=[ip, sender_port])
    sender.start()

def main():
    #test()
    test_with_router()

if __name__ == "__main__":
    main()