import socket
import threading
import time


clientlst = []
serverIP  = "192.168.0.200"
serverPort = 20001
bufferSize = 1024

msgFromServer = "Hello client"
byteToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)

UDPServerSocket.bind(serverIP,serverPort)
print("UDP Server up and listening")

def ReceiveThread():
    while True:
        byteAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = byteAddressPair[0].decode('utf-8')
        address = byteAddressPair[1]
        
        print(message)
        print(address)
        
        UDPServerSocket.sendto(byteToSend, address)
        
# Lắng nghe data
thread = threading.Thread(target = ReceiveThread, args= ())
thread.start()

while True:
    time.sleep(1)