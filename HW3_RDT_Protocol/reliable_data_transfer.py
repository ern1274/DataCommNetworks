import random
import socket
from multiprocessing import Process

from HW3_RDT_Protocol.sender_rdt import Sender, make_checksum
from HW3_RDT_Protocol.receiver_rdt import Receiver



def run_sender(ip, port):
    """Sets up Sender object with ip and port with predefined data
    and runs Sender function to send data to ip and port

    :param ip: ip address to send data to
    :param port: port number to send data to
    """
    print("Started Client")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender = Sender(soc, ip, port)
    data = [str(i) for i in range(30)]
    sender.arrange_pkts(data)
    sender.run_sender()
    print("Done with client")


def run_receiver(ip, port):
    """Sets up Receiver object to receive data from ip and port
    and puts received data in order within Receiver object

    :param ip: ip address to receive data from
    :param port: port number to receive data from
    """
    print("Started Server")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((ip,port))
    receiver = Receiver(soc)
    receiver.run_receiver()


def run_router(ip, sender_port, receiver_port):
    """Sets up a socket intended to middleman between
    Sender object and Receiver object,
    adding chances of packet loss and corruption to test receiver and sender
    interaction with lost packets and corrupted packets

    :param ip: ip address to get data from
    :param sender_port: port to receive data from sender
    :param receiver_port: port to receive data from receiver
    """
    print('Started Router')
    router_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    router_soc.bind((ip, sender_port))
    router_soc.settimeout(20)
    try:
        while True:
            sender_data, sender_address = router_soc.recvfrom(4096)
            if random.randint(0,100) > 90:
                print("Lost packet from sender to receiver")
                continue
            elif random.randint(0, 100) > 80:
                print("Corrupted pkt from sender to receiver")

                corrupted_msg = "corr".encode()
                corrupted_chksum = make_checksum(corrupted_msg)
                corrupted_msg = "corrupted".encode()
                sender_data = corrupted_chksum + corrupted_msg
                router_soc.sendto(sender_data, (ip, receiver_port))
                continue


            router_soc.sendto(sender_data, (ip,receiver_port))
            receiver_data, receiver_address = router_soc.recvfrom(4096)
            if random.randint(0,100) > 90:
                print("Lost packet from receiver to sender")
                continue

            elif random.randint(0, 100) > 80:
                print("Corrupted pkt from receiver to sender")

                corrupted_msg = "corr".encode()
                corrupted_chksum = make_checksum(corrupted_msg)
                corrupted_msg = "corrupted".encode()
                receiver_data = corrupted_chksum + corrupted_msg
                router_soc.sendto(receiver_data, sender_address)
                continue


            router_soc.sendto(receiver_data, sender_address)
    except:
        print("Messages have stopped, exiting router")

    return

def test_with_router():
    """Sets up router, receiver and sender processes to run simultaneously
    to allow interaction between all three processes

    """
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
    """Sets up receiver and sender processes to interact with each other

    """
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