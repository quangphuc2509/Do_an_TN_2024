import socket
import threading

msgFromclient = "Hello server"
byteToSend = str.encode(msgFromclient)
serverAddressPort = ("192.168.0.200", 20001)
bufferSize = 1024

clientIP = "192.168.0.200"
clientPort = 20015

UDPClientSocket = socket.socket(family= socket.AF_INET, type= socket.SOCK_DGRAM)
UDPClientSocket.bind(clientIP, clientPort)

print ("UDP CLient up and listening")