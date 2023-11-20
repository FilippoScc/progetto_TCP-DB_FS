import socket
import pickle
import facilities as F

def manage_list(s):
    s.send(' '.encode())
    data=s.recv(2048)
    data=F.bytes_to_list(data)
    for i in data:
        print(i)
    s.send(' '.encode())


HOST = 'localhost'    
PORT = 50007             
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    if data.decode()=="#99":
        manage_list(s)    
    else:
        print(data.decode())
    testo = input().encode()
    s.send(testo)




s.close()           