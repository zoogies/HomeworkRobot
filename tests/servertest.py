import socket


class tests:
    def connectTest(self, ip, port):
        try:
            return socket.getaddrinfo(ip, port)
        except:
            return "server failure"
