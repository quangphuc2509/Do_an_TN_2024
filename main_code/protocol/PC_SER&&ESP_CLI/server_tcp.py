import socket

SERVER_ID = socket.gethostbyname(socket.gethostname())
s = socket.socket()         
s.bind((SERVER_ID , 55555))
s.listen(0)                 
 
while True:
    client, addr = s.accept()
    while True:
        content = client.recv(32)
        if len(content) == 0:
            break
        else:
            print(content)
    print("Closing connection")  # This line prints a message indicating that the connection is being closed.
    client.close()