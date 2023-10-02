import os
import sys  # needed to access the command-line arguments
from socket import *

# socket buffer size
bufferSize = 1024

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

    global UDPSocket
    UDPSocket = socket(AF_INET, SOCK_DGRAM)

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
            print("Connection opened successfully.")

            while True:
                line, clientAddr2 = UDPSocket.recvfrom(bufferSize)

                #check if the client that sent the request is the one currently being catered to, if not then ignore it
                if clientAddr2 != clientAddr:
                    UDPSocket.sendto((msgNACK + " " + "Server currently occupied").encode(), clientAddr2)
                    print("Refused connection from a different client than the one with the connection open.")
                    continue

                arrLine = line.decode().split(" ")
                cmd = arrLine[0].lower()

                """ #Not needed, already verified on client side
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
                    print("Connection closed successfully.")
                    break  # To stop the loop

                else:
                    print("No Command: " + cmd)
        else:
            #print("No connection open yet. " + cmd)  # DEBUG
            UDPSocket.sendto((msgNACK + " Need to open connection first, your cmd = " + cmd).encode(), clientAddr)


def get(serverFileName, clientAddr, portNumber):
    try:
        serverFile = open("./" + serverFileName, "rb")
    except FileNotFoundError:
        # Handle error
        UDPSocket.sendto((msgNACK + " " + GET_SERVER_MISS_FILE).encode(), clientAddr)
        print("File request by client not found. File requested: " + serverFileName)
        return

    # Acknowledge client request
    UDPSocket.sendto(msgACK.encode(), clientAddr)

    # Connect to client by TCP
    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.connect((clientAddr[0], portNumber))

    # Read from file and send it to client
    fileBuffer = serverFile.read(bufferSize)
    while fileBuffer:
        TCPSocket.send(fileBuffer)  # File was opened in binary mode, so no need to encode()
        fileBuffer = serverFile.read(bufferSize)

    # Close the TCP connection and close the file
    # Recommended by python documentation to shutdown() before close() for faster connection closing
    TCPSocket.shutdown(SHUT_RDWR)
    TCPSocket.close()
    serverFile.close()

    print("File transfer successful. File: " + serverFileName + " sent to client.")


def put(serverFileName, clientAddr, portNumber):
    if os.path.exists("./" + serverFileName):  # Handle error
        UDPSocket.sendto((msgNACK + " " + PUT_SERVER_EXISTS_FILE).encode(), clientAddr)
        return

    # Create and open the file to put in the server
    serverFile = open("./" + serverFileName, "wb")

    # Acknowledge client request
    UDPSocket.sendto(msgACK.encode(), clientAddr)

    # Connect to client by TCP
    TCPSocket = socket(AF_INET, SOCK_STREAM)
    TCPSocket.connect((clientAddr[0], portNumber))

    # Receive the file sent by the client and write it to the newly created file
    fileBuffer = TCPSocket.recv(bufferSize)
    while fileBuffer:
        serverFile.write(fileBuffer)  # The file was opened in binary mode, so no need to decode
        fileBuffer = TCPSocket.recv(bufferSize)

    # Close the TCP connection and close the file
    TCPSocket.close()
    serverFile.close()

    print("File transfer successful. File: " + serverFileName + " received from client.")


if __name__ == "__main__":  # Check if the module is being run as the main program
    main()
