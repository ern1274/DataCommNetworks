import socket
from multiprocessing import Process
from HW3_RDT_Protocol.receiver_rdt import Receiver
from HW3_RDT_Protocol.sender_rdt import Sender


def make_packets(file_name, chunk_size):
    """Forms packets from file by splitting file into chunks

    :param file_name: String containing name of file to send
    :type file_name: String
    :param chunk_size: number of characters to fit in a chunk from file
    :type chunk_size: int
    :return: pkts, array of character chunks from file
    :rtype: Array
    """
    file = open(file_name, 'r')
    content = file.read()
    file.close()
    pkts = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    print(pkts)
    return pkts

def send_file(file_name, ip, port):
    """Forms packets from file by splitting file into chunks

    :param file_name: String containing name of file to send
    :type file_name: String
    :param ip: ip address to send file to
    :type ip: string
    :param port: port number to send file to
    :type port: int
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender = Sender(soc, ip, port)
    sender.arrange_pkts(make_packets(file_name, 15))
    sender.run_sender()
    print("Sent file")
    return

def write_file(file_name, pkts):
    """joins packets from sender and writes to file

    :param file_name: String containing name of file to write to
    :type file_name: String
    :param pkts: array of character chunks from file
    :type pkts: Array
    """
    file = open(file_name, 'w')
    content = ''.join(pkts)
    file.write(content)
    file.close()
    return

def receive_file(file_name, ip, port):
    """Gets packets from sender and puts together packets to form a file

    :param file_name: String containing name of file to receive
    :type file_name: String
    :param ip: ip address to receive file from
    :type ip: string
    :param port: port number to receive file from
    :type port: int
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((ip, port))
    receiver = Receiver(soc)
    receiver.run_receiver()
    pkts = receiver.get_packets()
    new_file_name = 'recv_' + file_name
    write_file(new_file_name, pkts)
    return

def main():
    file_name = 'seven_old_samurai.txt'
    ip = '127.0.0.1'
    port = 5000
    #send_file(file_name, ip, port)


    sender = Process(target=send_file, args=[file_name, ip, port])
    sender.start()
    receiver = Process(target=receive_file, args=[file_name, ip, port])
    receiver.start()

if __name__ == "__main__":
    main()