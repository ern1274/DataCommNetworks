import socket
import sys
from multiprocessing import Process

ip = '127.0.0.1'
port = 5000
def run_client():
    print("Started Client")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = "Hello There"
        soc.sendto(message.encode(), (ip, port))
        data, address = soc.recvfrom(4096)
        print("Client Received: " + data.decode())

def run_server():
    print("Started Server")
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind((ip,port))

    while True:
        data, address = soc.recvfrom(4096)
        data_string = data.decode()
        print("Server Received: " + data_string + " from " + str(address))
        message = "Acknowledged"
        soc.sendto(message.encode(), address)

def run_router():
    return

def main():

    server = Process(target=run_server)
    server.start()

    client = Process(target=run_client)
    client.start()

if __name__ == "__main__":
    main()