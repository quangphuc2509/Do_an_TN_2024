import socket
import threading
from time import sleep 

PORT = 55555  
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.0.200'
ADDR = (SERVER, PORT)

client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(ADDR)
connected = True


#create thread that will receive data from server

# what is the thread??
# thread is programme which is run in parallel with main programme 
def handle_rev(client_tcp):
    while connected:
        msg = client_tcp.recv(25).decode(FORMAT)
        print(msg)
        print(len(msg))

def send(msg):
    if isinstance(msg, str):
        message = msg
    else:
        message = f'{msg:.2f}'
    client_tcp.send(message.encode(FORMAT))

thread = threading.Thread(target=handle_rev, args=(client_tcp,))
thread.start()

while True:
    send('xin chao day la van toc cua xe: 1.2124235345345345345345 va day la vi tri cua xe: x: 4.128290492783472 y: 28.32478128912912373734, khoang cach la: 21922') 
    sleep(0.1)

send(DISCONNECT_MESSAGE)
connected = False
thread.join()
