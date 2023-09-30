# print("Hello Client World!")
import os   # useful to check if file exists in the directory
from socket import *
import sys  # needed to access the command-line arguments

# socket buffer size
bufferSize = 1024

global serverAddressPort
global clientSocket
global UDPClientSocket

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
    len_args = len(sys.argv)  # get number of arguments
    if len_args != 3:
        (print("Wrong number of arguments please put only the server " +
               "name and the UDP Port so the server can receive commands"))
        sys.exit(6969)
    else:
        serverName = sys.argv[1]
        serverPort = sys.argv[2]
        serverAddressPort = (serverName, int(serverPort))
        # print("server port: ", serverPort)  # after that check if the port is valid

    # create UDP socket
    UDPClientSocket = socket(AF_INET, SOCK_DGRAM)
    # create TCP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # open TCP connection
    clientSocket.connect(serverAddressPort)

    while True:
        line = input("-> ")
        arrLine = line.split(" ")  # Array with the input
        cmd = arrLine[0]
        numArg = len(arrLine) - 1  # Don't count the name of the command

        if cmd == msgOPEN:
            if numArg != 1:  # Check number of arguments
                print("Invalid number of arguments.")
            else:
                numPort = int(arrLine[1])
                # Check if port number is valid
                if numPort < MIN_PORT_NUMBER or numPort > MAX_PORT_NUMBER:
                    print("Invalid Port Number.")
                    continue

                openConnection(arrLine[1])

        elif cmd == msgGET:
            if numArg != 2:  # Check number of arguments
                print("Invalid number of arguments.")
                continue

            serverFileName = arrLine[1]
            clientFileName = arrLine[2]
            getFileFromServer(serverFileName, clientFileName)

        elif cmd == msgPUT:
            if numArg != 2:  # Check number of arguments
                print("Invalid number of arguments.")
                continue

            clientFileName = arrLine[1]
            serverFileName = arrLine[2]
            putFileInServer(serverFileName, clientFileName)

        elif cmd == msgCLOSE:
            closeConnection()
            break  # To stop the loop

        else:
            print("No Command: " + cmd)


# Request Server to open TCP Connection
def openConnection(port):
    # Sends the request to the server
    UDPClientSocket.sendto((msgOPEN + "" + port).encode(), serverAddressPort)
    # Receives the confirmation or denial of the request
    msgFromServer = (UDPClientSocket.recvfrom(bufferSize)).decode()

    if msgFromServer == msgNACK:  # Denial handling
        print("ERROR: Server didn't acknowledge request for an unknown reason.")
    elif msgFromServer != msgACK:  # Unknown answer from the server handling
        print("ERROR: Unknown answer from server.")


# Close the TCP Connection and tell server to do the same
def closeConnection():
    #Sends the request to the server
    UDPClientSocket.sendto(msgCLOSE.encode(), serverAddressPort)
    #Receives the confirmation or denial of the request
    msgFromServer = (UDPClientSocket.recvfrom(bufferSize)).decode()

    if msgFromServer == msgNACK: #  Denial handling
        print("ERROR: Server didn't acknowledge request for an unknown reason.")
    elif msgFromServer != msgACK: #  Unknown answer from the server handling
        print("ERROR: Unknown answer from server.")
    else:
        clientSocket.close()


def getFileFromServer(serverFileName, clientFileName):

    # Verifies if the file exists
    if os.path.exists("./clientFiles/" + clientFileName):
        print("A file with the indicated name already exists on the client.")
        return

    # Sends the request to the server
    UDPClientSocket.sendto((msgGET + " " + serverFileName).encode(), serverAddressPort)

    # Receives the confirmation or denial of the request
    msgFromServer = ((UDPClientSocket.recvfrom(bufferSize)).decode()).split(" ")

    # Denial handling
    if msgFromServer[1] != msgACK:
        if msgFromServer[1] == msgNACK:
            if msgFromServer[2] == GET_SERVER_ERROR_FILE:
                print("The requested file does not exist on server")
            else:
                print("ERROR: Server didn't acknowledge request for an unknown reason.")
        else:
            print("ERROR: Unknown answer from the server.")
        return

    # Receiving from the server and writing to the clientFile
    clientFile = open("./clientFiles/" + clientFileName, "wb")

    fileBuffer = clientSocket.recv(bufferSize)  # The file was opened in binary mode, so no need to decode
    while fileBuffer:
        clientFile.write(fileBuffer)
        fileBuffer = clientSocket.recv(bufferSize)

    # Closing the socket ??????? and Closing the file
    """   #nao apagues isto ate termos a certeza
    clientSocket.close()
    """
    clientFile.close()

    print("File download complete: file " + serverFileName +
          " from the server is " + clientFileName + "in the client.")


def putFileInServer(serverFileName, clientFileName): # TODO
    # Opens the file if it exists
    try:
        clientFile = open("./clientFiles/" + clientFileName, "rb")
    except FileNotFoundError:
        print("The indicated file does not exist on the client.")
        return

    # Sends the request to the server
    UDPClientSocket.sendto((msgPUT + " " + serverFileName).encode(), serverAddressPort)

    # Receives the confirmation or denial of the request
    msgFromServer = ((UDPClientSocket.recvfrom(bufferSize)).decode()).split(" ")

    # Denial Handling
    if msgFromServer[1] != msgACK:
        if msgFromServer[1] == msgNACK:
            if msgFromServer[2] == PUT_SERVER_ERROR_FILE:
                print("A file with the indicated name already exists on the server")
            else:
                print("ERROR: Server didn't acknowledge request for an unknown reason.")
        else:
            print("ERROR: Unknown answer from the server.")
        return

    # Send file to the server
    fileBuffer = clientFile.read(bufferSize)  # The file was opened in binary mode, so no need to encode

    while fileBuffer:
        clientSocket.send(fileBuffer)
        fileBuffer = clientFile.read(bufferSize)

    # Closing the socket ??????? and Closing the file
    """   #nao apagues isto ate termos a certeza
    clientSocket.shutdown(SHUT_RDWR);
    clientSocket.close()
    """
    clientFile.close()

    print("File upload complete: file " + clientFileName +
          " from the client is " + serverFileName + "in the server.")


# Check if the module is being run as the main program
# if it is then the program starts here
if __name__ == "__main__":
    main()
