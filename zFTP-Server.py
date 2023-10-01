import os
import sys  # needed to access the command-line arguments
from socket import *

# socket buffer size
bufferSize = 1024

# creating UDP socket
UDPSocket = socket(AF_INET, SOCK_DGRAM)

serverName = "127.0.0.1"
msgCLOSE = "close"
msgOPEN = "open"
msgGET = "get"
msgPUT = "put"
msgACK = "ack"
msgNACK = "nack"
PUT_SERVER_EXISTS_FILE = "3"
GET_SERVER_MISS_FILE = "3"
MIN_PORT_NUMBER = 1024
MAX_PORT_NUMBER = 65535



def main():

    print("Server is Listening")

    # check number of arguments
    len_args = len(sys.argv)
    if len_args != 2:
        print("Wrong number of arguments.")
        return

    #print("Server port", sys.argv[1])  # DEBUG

    # bind UDP socket
    serverAddressPort = (serverName, int(sys.argv[1]))
    UDPSocket.bind(serverAddressPort)

    #run server operations
    while True:
        line, clientAddr = UDPSocket.recvfrom(bufferSize)
        arrLine = line.decode().split(" ")  # Array with the input
        cmd = arrLine[0]

        # Open connection with a Client
        if cmd == msgOPEN:
            portNumber = int(arrLine[1])
            UDPSocket.sendto(msgACK.encode(), clientAddr)

            while True:
                line, clientAddr2 = UDPSocket.recvfrom(bufferSize)

                #check if the client that sent the request is the one currently being catered to, if not then ignore it
                if clientAddr2 != clientAddr:
                    UDPSocket.sendto((msgNACK + " " + "Server currently occupied").encode(), clientAddr2)
                    continue

                arrLine = line.decode().split(" ")
                cmd = arrLine[0]

                """
                if cmd == msgOPEN: #check if the open connection is called with the same port
                    UDPSocket.sendto((msgNACK + " This connection is already open").encode(), clientAddr)
                """

                if cmd == msgGET:
                    serverFileName = arrLine[1]
                    get(serverFileName, clientAddr, portNumber)

                elif cmd == msgPUT:
                    serverFileName = arrLine[1]
                    put(serverFileName, clientAddr, portNumber)

                elif cmd == msgCLOSE:
                    UDPSocket.sendto(msgACK.encode(), clientAddr)
                    print("connection is closed")
                    break  # To stop the loop

                else:
                    print("No Command: " + cmd)
        else:
            print("No connection open yet. " + cmd)  # DEBUG
            UDPSocket.sendto((msgNACK + " Need to open first, cmd = " + cmd).encode(), clientAddr)


def get(serverFileName, clientAddr, portNumber):
    try:
        serverFile = open("./serverFiles/" + serverFileName, "rb")
    except FileNotFoundError:
        UDPSocket.sendto((msgNACK + " " + GET_SERVER_MISS_FILE).encode(), clientAddr)
        return

    UDPSocket.sendto(msgACK.encode(), clientAddr)

    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.connect((clientAddr[0], portNumber))

    fileBuffer = serverFile.read(bufferSize)

    while fileBuffer:
        TCPSocket.send(fileBuffer)
        fileBuffer = serverFile.read(bufferSize)

    TCPSocket.shutdown(SHUT_RDWR) #shutdown of the connection of the socket
    TCPSocket.close()
    serverFile.close()


def put(serverFileName, clientAddr, portNumber):
    if os.path.exists("./serverFiles/" + serverFileName):
        UDPSocket.sendto((msgNACK + " " + PUT_SERVER_EXISTS_FILE).encode(), clientAddr)
        return

    serverFile = open("./serverFiles/" + serverFileName, "wb")

    UDPSocket.sendto(msgACK.encode(), clientAddr)

    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.connect((clientAddr[0], portNumber))

    fileBuffer = TCPSocket.recv(bufferSize)  # The file was opened in binary mode, so no need to decode
    while fileBuffer:
        serverFile.write(fileBuffer)
        fileBuffer = TCPSocket.recv(bufferSize)

    TCPSocket.close()
    serverFile.close()



if __name__ == "__main__":  #check if the module is being run as the main program
    main()
