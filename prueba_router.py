import sys
import socket

headers = sys.argv[1]
ip_inicial = sys.argv[2]
port_inicial = int(sys.argv[3])

file = open("test.txt","r")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while(True):
    data = file.readline()
    if not data:
        break
    else:
        data = headers+","+data
        data = data.encode()
        sock.sendto(data, (ip_inicial, port_inicial))
print("done")