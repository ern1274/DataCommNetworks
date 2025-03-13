import socket
import threading
import time
import zlib
import struct



def make_checksum(data):
    return zlib.crc32(data).to_bytes(8,'big',signed=True)

def make_sender_payload(seq_num, msg):
    seq_bytes = seq_num.to_bytes(4, byteorder='big', signed=True)
    msg_bytes = msg.encode()
    payload = seq_bytes + msg_bytes
    return payload

def convert_receiver_payload(data):
    send_seq = int.from_bytes(data[:4], byteorder='big', signed=True)
    msg = data[4:].decode()
    return send_seq, msg

def verify_integrity(sent_chksum, data):
    chksum = make_checksum(data)
    return sent_chksum == chksum

def make_packet(seq_num, msg):
    payload = make_sender_payload(seq_num, msg)
    chksum = make_checksum(payload)
    return chksum+payload

class Sender:
    packets = None
    def __init__(self, soc, ip, port):
        self.soc = soc
        self.ip = ip
        self.port = port
        self.base_seq = 1

    def send_pkt(self, seq_num):
        print("Retransmitting " + str(seq_num) + " to " + str(self.ip) + " : "+ str(self.port))
        self.soc.sendto(self.packets[seq_num - self.base_seq][0], (self.ip, self.port))
        self.packets[seq_num- self.base_seq][2] = threading.Timer(5.0, self.send_pkt, [seq_num])
        self.packets[seq_num- self.base_seq][2].start()

    def arrange_pkts(self, data):
        self.packets = []
        seq_num = self.base_seq
        msg = 'Communication'
        for pkt in data:
            #print(pkt)
            packet = make_packet(seq_num, msg)
            self.packets.append([packet, False,
                                 threading.Timer(5.0, self.send_pkt, [seq_num])])
            seq_num += 1


    def find_recv_base_window(self, window_size):
        for i in range(len(self.packets)):
            if not self.packets[i][1]:
                if i + window_size >= len(self.packets):
                    #print("returning: " + str(i) + " and " + str(len(self.packets)-1))
                    return i, len(self.packets)-1
                else:
                    #print("returning: " + str(i) + " and " + str(i + window_size))
                    return i, i + window_size
        return None, None

    def run_sender(self):
        win_size = int(len(self.packets) / 4)
        recv_base, win_end = self.find_recv_base_window(win_size)
        while recv_base is not None:
            for i in range(recv_base, win_end+1):
                if not (self.packets[i][2].finished.is_set() or self.packets[i][2].is_alive()):
                    print("Transmitting " + str(self.base_seq + i))
                    payload = self.packets[i][0]
                    self.soc.sendto(payload, (self.ip, self.port))
                    self.packets[i][2].start()
                    time.sleep(0.2)

            self.soc.settimeout(1)
            try:
                while True:
                    data, address = self.soc.recvfrom(4096)
                    chksum = data[:8]
                    data = data[8:]
                    if verify_integrity(chksum, data):
                        recv_seq, ack = convert_receiver_payload(data)
                        print('Client confirming packet ' + str(recv_seq))
                        if not self.packets[recv_seq - self.base_seq][1]:
                            self.packets[recv_seq - self.base_seq][1] = True
                        self.packets[recv_seq - self.base_seq][2].cancel()
                        #self.packets[recv_seq - self.base_seq][2].join()
            except:
                self.soc.settimeout(None)
                recv_base, win_end = self.find_recv_base_window(win_size)
                continue

        while True:
            payload = make_packet(-1,'FIN')
            self.soc.sendto(payload, (self.ip, self.port))
            self.soc.settimeout(10)
            try:
                data, address = self.soc.recvfrom(4096)
                chksum = data[:8]
                data = data[8:]
                if verify_integrity(chksum, data):
                    recv_seq, ack = convert_receiver_payload(data)
                    if recv_seq == -1:
                        break
            except:
                continue


        print("ACKed end of data, now exiting")
        return
