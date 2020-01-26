import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("10.129.15.116", 8000))
# s.connect(('127.0.0.1', 9090))


files = open('log.txt', 'a')
while True:
    data = s.recv(64)
    print(str(data))
    print(str(data)[2:-1])
    files.write(str(data)[2:-1] + '\n')
