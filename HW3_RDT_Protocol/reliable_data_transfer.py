import socket
import sys
from multiprocessing import Process
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1, send, sniff

ip = '127.0.0.1'
port = 5000
def run_sender():
    print("Started Client")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #soc.settimeout(1)

    seq_num = 1
    ack_bit = False
    msg = "Hello There"


    #while True:
    while seq_num < 50:
        # T1/T4
        payload = make_sender_payload(seq_num, ack_bit, msg)
        soc.sendto(payload, (ip, port))

        soc.settimeout(1)
        try:
            data, address = soc.recvfrom(4096)
            recv_seq, recv_msg = convert_receiver_payload(data)
            print("Receiver Sequence Number: " + str(recv_seq))
            print("Client Received: " + recv_msg + " from " + str(address))
            #T2/T5
            if not (verify_integrity() and recv_seq == seq_num and recv_msg == 'ACK'):
                continue
            #T3/T6
            else:
                seq_num += 1
                ack_bit = not ack_bit
        except socket.timeout:
            print("Timed out")
            continue

def make_sender_payload(seq_num, pkt_bit, msg):
    pkt_bit = int(pkt_bit)
    seq_bytes = seq_num.to_bytes(4, byteorder='big')
    pkt_bytes = pkt_bit.to_bytes(4, byteorder='big')
    msg_bytes = msg.encode()
    payload = seq_bytes + pkt_bytes + msg_bytes
    return payload

def convert_sender_payload(data):
    send_seq = int.from_bytes(data[:4], byteorder='big')
    pkt_bit = int.from_bytes(data[4:8], byteorder='big')
    msg = data[8:].decode()
    return send_seq, pkt_bit, msg


def run_receiver():
    print("Started Server")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((ip,port))
    #soc.settimeout(1)
    seq_num = -1
    ack_bit = False

    while True:
        data, address = soc.recvfrom(4096)
        send_seq, sender_bit, msg = convert_sender_payload(data)
        print("Client Sequence Number: " + str(send_seq))
        print("Client Packet bit: " + str(sender_bit))
        print("Server Received: " + msg + " from " + str(address))
        if seq_num == -1: # Not yet established
            seq_num = send_seq

        # T1/T4
        if verify_integrity() and sender_bit == int(ack_bit):
            # Add data to buffer
            msg = "ACK"
            payload = make_receiver_payload(seq_num, msg)
            soc.sendto(payload, address)
            seq_num += 1
            ack_bit = not ack_bit

        # T2/T5
        elif verify_integrity() and sender_bit != int(ack_bit):
            msg = "ACK"
            payload = make_receiver_payload(send_seq, msg)
            soc.sendto(payload, address)
        #T3/T6
        else:
            msg = "ACK"
            payload = make_receiver_payload(seq_num-1, msg)
            soc.sendto(payload, address)


def make_receiver_payload(seq_num, msg):
    seq_bytes = seq_num.to_bytes(4, byteorder='big')
    msg_bytes = msg.encode()
    payload = seq_bytes + msg_bytes
    return payload

def convert_receiver_payload(data):
    send_seq = int.from_bytes(data[:4], byteorder='big')
    msg = data[4:].decode()
    return send_seq, msg

def verify_integrity():
    return True

def run_router():
    return

def main():
    receiver = Process(target=run_receiver)
    receiver.start()

    sender = Process(target=run_sender)
    sender.start()

if __name__ == "__main__":
    main()