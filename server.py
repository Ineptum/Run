import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("10.129.15.116", 5000))
# s.connect(('127.0.0.1', 9090))

with open("log.txt", "w") as file:
    file.write('')

while True:
    data = s.recv(64)
    with open("log.txt", "a+") as file:
        file.write(str(data).lstrip("b'").rstrip("'") + "\n")
