import os
import sys  #needed to access the command-line arguments
from socket import *

# socket buffer size
bufferSize = 1024

global serverAddressPort
#global TCPSocket
global UDPSocket

serverName = "127.0.0.1"
msgCLOSE = "close"
msgOPEN = "open"
msgGET = "get"
msgPUT = "put"
msgACK = "ack"
msgNACK = "nack"
PUT_SERVER_ERROR_FILE = "3"
GET_SERVER_ERROR_FILE = "3"
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

    open = False

    while True:
        line, clientAddr = UDPSocket.recvfrom(bufferSize)
        arrLine = line.decode().split(" ")  # Array with the input
        cmd = arrLine[0]

        if cmd == msgOPEN:
            portNumber = int(arrLine[1])

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

                elif cmd == msgGET:
                    serverFileName = arrLine[1]
                    if not os.path.exists("./serverFiles/" + serverFileName):
                        UDPSocket.sendto((msgNACK + " " + GET_SERVER_ERROR_FILE).encode(), clientAddr)
                        break

                    get(serverFileName, portNumber)

                elif cmd == msgPUT:
                    serverFileName = arrLine[1]
                    #putFileInServer(serverFileName, clientFileName)

                elif cmd == msgCLOSE:
                    break  # To stop the loop

                else:
                    print("No Command: " + cmd)


def get(serverFileName, portNumber):
    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.bind(serverAddressPort)
    TCPSocket.listen(1)

    connSocket, addr = TCPSocket.accept()


if __name__ == "__main__":  #check if the module is being run as the main program
    main()