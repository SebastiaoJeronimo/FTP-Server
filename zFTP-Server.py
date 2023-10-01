import os
import sys  #needed to access the command-line arguments
from socket import *

# socket buffer size
bufferSize = 1024

#global serverAddressPort
#global UDPSocket

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

    print("Hello Server World!")

    len_args = len(sys.argv)  # get number of arguments
    if len_args != 2:
        print ("wrong number of arguments please put only the UDP Port so the server can receive commands")
        return

    print("server port" , sys.argv[1])  # after that check if the port is valid

    """ ja verificamos o server port antes e nao ha mais nenhum argumento 
    
    print("Number of arguments: ",len_args-1) #nem para debug é necessario pq ja verificamos antes
    print("Argument list: ")
    for i in range(1, len_args):    #list all arguments
        print(str(sys.argv[i]))
    """

    serverAddressPort = (serverName, int(sys.argv[1]))

    # create UDP socket
    UDPSocket = socket(AF_INET, SOCK_DGRAM)
    UDPSocket.bind(serverAddressPort)

    while True:
        line, clientAddr = UDPSocket.recvfrom(bufferSize)
        arrLine = line.decode().split(" ")  # Array with the input
        cmd = arrLine[0]

        if cmd == msgOPEN:
            portNumber = int(arrLine[1])
            UDPSocket.sendto(msgACK.encode(), clientAddr)

            while True:
                line, clientAddr2 = UDPSocket.recvfrom(bufferSize)
                #check if the client that sent the request is the one currently being catered to, if not then ignore it
                if clientAddr2 != clientAddr:
                    UDPSocket.sendto((msgNACK + " " + "Server currently occupied").encode(), clientAddr2)
                    continue

                arrLine = line.decode().split(" ")  # Array with the input
                cmd = arrLine[0]

                if cmd == msgOPEN:  # DEBUG
                    print("Can't open a second connection")
                    UDPSocket.sendto((msgNACK + " This connection is already open").encode(), clientAddr)

                elif cmd == msgGET:
                    serverFileName = arrLine[1]
                    get(UDPSocket, serverFileName, clientAddr, portNumber)

                elif cmd == msgPUT:
                    serverFileName = arrLine[1]
                    put(UDPSocket, serverFileName, clientAddr, portNumber)

                elif cmd == msgCLOSE:
                    UDPSocket.sendto(msgACK.encode(), clientAddr)
                    break  # To stop the loop

                else:
                    print("No Command: " + cmd)
        else:
            print("No connection open yet. " + cmd)  # DEBUG
            UDPSocket.sendto((msgNACK + " Need to open first, cmd = " + cmd).encode(), clientAddr)


def get(UDPSocket, serverFileName, clientAddr, portNumber):
    try:
        serverFile = open("./serverFiles/" + serverFileName, "rb")
    except FileNotFoundError:
        UDPSocket.sendto((msgNACK + " " + GET_SERVER_MISS_FILE).encode(), clientAddr)
        return

    UDPSocket.sendto(msgACK.encode(), clientAddr)

    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.connect(("127.0.0.2", portNumber))

    fileBuffer = serverFile.read(bufferSize)

    while fileBuffer:
        TCPSocket.send(fileBuffer)
        fileBuffer = serverFile.read(bufferSize)

    TCPSocket.shutdown(SHUT_RDWR)
    TCPSocket.close()
    serverFile.close()


def put(UDPSocket, serverFileName, clientAddr, portNumber):
    if os.path.exists("./serverFiles/" + serverFileName):
        UDPSocket.sendto((msgNACK + " " + PUT_SERVER_EXISTS_FILE).encode(), clientAddr)
        return

    serverFile = open("./serverFiles/" + serverFileName, "wb")

    UDPSocket.sendto(msgACK.encode(), clientAddr)

    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.connect(("127.0.0.2", portNumber))

    fileBuffer = TCPSocket.recv(bufferSize)  # The file was opened in binary mode, so no need to decode
    while fileBuffer:
        serverFile.write(fileBuffer)
        fileBuffer = TCPSocket.recv(bufferSize)

    TCPSocket.close()
    serverFile.close()



if __name__ == "__main__":  #check if the module is being run as the main program
    main()