'''
import socket
import threading
import os

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.accept_connections()

    def accept_connections(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter desired port --> '))

        self.s.bind((ip,port))
        self.s.listen(100)

        print('Running on IP: '+ip)
        print('Running on port: '+str(port))

        while 1:
            c, addr = self.s.accept()
            print(c)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def handle_client(self,c,addr):
        data = c.recv(1024).decode()

        if not os.path.exists(data):
            c.send("file-doesn't-exist".encode())

        else:
            c.send("file-exists".encode())
            print('Sending',data)
            if data != '':
                file = open(data,'rb')
                data = file.read(1024)
                while data:
                    c.send(data)
                    data = file.read(1024)

                c.shutdown(socket.SHUT_RDWR)
                c.close()


server = Server()
'''
"""
Server receiver of the file
"""
import socket

import os

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 6045
# receive 4096 bytes each time
BUFFER_SIZE = 4096
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()

filename1 = os.path.basename(received)
print("path is",os.path.basename(filename1))
print("filname is ", received)
print("Current sir",os.getcwd())
print("list directory ",os.listdir())
print("list of permision", os.stat('test.txt'))
with open("mytext.txt", "wb+") as sf:
    sf.write("this is sample file")
os.chmod("mytext.txt", 777)


with open(filename1, "wb+") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
client_socket.close()
s.close()