#print("Hello Client World!")


from socket import *

serverName = "localhost"            # server name
serverPort = 12000                  # socket server port number
sockBuffer = 2048                   # socket buffer size

def main():
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection