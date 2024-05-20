import socket
import threading

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) # create address client
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# create thread to receiving data from client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True 
    while connected: 
        msg = conn.recv(1024).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False 
        
        print(f"[{addr}] {msg}")
        print(len(msg))
        message = msg
        # conn.send(message.encode(FORMAT)) # if server receives , server will send data to client
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        thread.join()

print("[STARTING] Server is starting...")
start()
       