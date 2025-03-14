import zlib

def make_checksum(data):
    return zlib.crc32(data).to_bytes(8,'big',signed=True)

def make_receiver_payload(seq_num, msg):
    seq_bytes = seq_num.to_bytes(4, byteorder='big', signed=True)
    msg_bytes = msg.encode()
    payload = seq_bytes + msg_bytes
    return payload

def convert_sender_payload(data):
    send_seq = int.from_bytes(data[:4], byteorder='big', signed=True)
    msg = data[4:].decode()
    return send_seq, msg

def verify_integrity(sent_chksum, data):
    chksum = make_checksum(data)
    return sent_chksum == chksum

def make_packet(seq_num, msg):
    payload = make_receiver_payload(seq_num, msg)
    chksum = make_checksum(payload)
    return chksum+payload

class Receiver:
    packets = []
    base_seq = -1
    max_seq = -1

    def __init__(self, soc):
        self.soc = soc

    # Rebase and add pkt function will change base_seq and max_seq
    def add_packet(self, seq_num,data, expand_pkts):
        if expand_pkts:
            until_seq = seq_num - self.max_seq
            for i in range(until_seq):
                self.packets.append(None)
            self.max_seq = seq_num
        self.packets[seq_num - self.base_seq] = data
        return

    def rebase_packets(self, seq_num, data):
        until_base = self.base_seq - seq_num
        for i in range(until_base):
            self.packets.insert(0, None)
        self.base_seq = seq_num
        self.packets[self.base_seq - self.base_seq] = data
        return

    def get_packets(self):
        return self.packets

    def clear_packets(self):
        self.packets.clear()
        return

    def run_receiver(self):
        print("Started Server")
        try:
            while True:
                data, address = self.soc.recvfrom(4096)
                chksum = data[:8]
                data = data[8:]
                if verify_integrity(chksum, data):
                    send_seq, msg = convert_sender_payload(data)
                    print("Server Received seq: " + str(send_seq))
                    print("The message is: " + msg)
                    if send_seq == -1:
                        print("Client is done, sending ack")
                        self.soc.sendto(make_packet(send_seq, "ACK"), address)
                        print(self.get_packets())
                        self.soc.settimeout(15)
                        continue

                    if self.base_seq == -1:
                        print("Server Establishing base and max seq as " + str(send_seq))
                        self.base_seq = send_seq
                        self.max_seq = send_seq
                        self.packets = [None]

                    if send_seq < self.base_seq:
                        print("Server rebasing packets where base_seq: " + str(self.base_seq) + " to " + str(send_seq))
                        self.rebase_packets(send_seq, msg)
                    elif send_seq >= self.max_seq:
                        print("Server expanding packets from max_seq: " + str(self.max_seq) + " to " + str(send_seq))
                        self.add_packet(send_seq, msg, True)
                    elif send_seq < self.max_seq and self.packets[send_seq - self.base_seq] is None:
                        self.add_packet(send_seq, msg, False)

                    self.soc.sendto(make_packet(send_seq, "ACK"), address)
                else:
                    print("Corrupted packet, discarding")
        except:
            print("Getting no more messages, exiting receiver")
        return


