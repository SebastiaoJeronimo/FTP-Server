# print("Hello Client World!")
import os   # useful to check if file exists in the directory
from socket import *
import sys  # needed to access the command-line arguments

#
bufferSize = 1024
MIN_PORT_NUMBER = 1024
MAX_PORT_NUMBER = 65535

# Input keywords
msgCLOSE = "close"
msgOPEN = "open"
msgGET = "get"
msgPUT = "put"
msgQUIT = "quit"

# Server response keywords
msgACK = "ack"
msgNACK = "nack"

# Server response Errors
PUT_SERVER_EXISTS_FILE = "3"
GET_SERVER_MISS_FILE = "3"

# create TCP/UDP sockets



def main():
    len_args = len(sys.argv)
    # Check number of arguments
    if len_args != 3:
        print("Wrong number of arguments.")
        sys.exit(6969)

    serverName = sys.argv[1]
    serverPort = sys.argv[2]
    serverAddressPort = (serverName, int(serverPort))

    # Declaring TCP/UDP sockets as global variables
    global clientSocket
    global UDPClientSocket
    UDPClientSocket = socket(AF_INET, SOCK_DGRAM)

    opened = False

    print("Client is waiting for commands.")

    while True:
        line = input("-> ")
        arrLine = line.split(" ")  # Array with the input
        cmd = arrLine[0].lower()
        numArg = len(arrLine) - 1  # Don't count the name of the command

        #print("arrLine: " ) # DEBUG
        #print(arrLine)

        if cmd == msgOPEN:
            if opened:
                print("Connection with server already open.")
                continue
            if numArg != 1:  # Check number of arguments
                print("Invalid number of arguments.")
                continue

            numPort = int(arrLine[1])
            # Check if port number is valid
            if numPort < MIN_PORT_NUMBER or numPort > MAX_PORT_NUMBER or numPort == serverAddressPort[1]:
                print("Invalid Port Number.")
                continue

            clientSocket = socket(AF_INET, SOCK_STREAM)
            opened = openConnection(serverAddressPort, arrLine[1])

        elif cmd == msgGET:
            if not opened:
                print("To get a file you must first open a connection with the server.")
                continue
            if numArg != 2:  # Check number of arguments
                print("Invalid number of arguments.")
                continue

            serverFileName = arrLine[1]
            clientFileName = arrLine[2]
            getFileFromServer(serverAddressPort, serverFileName, clientFileName)

        elif cmd == msgPUT:
            if not opened:
                print("To put a file you must first open a connection with the server.")
                continue
            if numArg != 2:  # Check number of arguments
                print("Invalid number of arguments.")
                continue

            clientFileName = arrLine[1]
            serverFileName = arrLine[2]
            putFileInServer(serverAddressPort, serverFileName, clientFileName)

        elif cmd == msgCLOSE:
            if not opened:
                print("There is no connection to server.")
            else:
                opened = closeConnection(serverAddressPort)

        elif cmd == msgQUIT:
            if opened:
                print("Connection with server still open, close it to be able to quit.")
            else:
                break  # To stop the loop

        else:
            print("Command: " + cmd + " does not exist.")


# Request Server to open TCP Connection
def openConnection(serverAddressPort, port):
    # Sends the request to the server
    UDPClientSocket.sendto((msgOPEN + " " + port).encode(), serverAddressPort)
    # Receives the confirmation or denial of the request
    msgFromServer, trash = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = msgFromServer.decode()

    if msgFromServer == msgNACK:
        print("ERROR: Server didn't acknowledge request for an unknown reason.")
        return False
    elif msgFromServer != msgACK:
        print("ERROR: " + msgFromServer)
        return False

    # DEBUG
    #print("Received msg from server: " + msgFromServer)

    #clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.bind((UDPClientSocket.getsockname()[0], int(port)))
    clientSocket.listen(1)  # only accepts one connection at a time
    print("Connection with server is open.")
    return True


# Close the TCP Connection and tell server to do the same
def closeConnection(serverAddressPort):
    #Sends the request to the server
    UDPClientSocket.sendto(msgCLOSE.encode(), serverAddressPort)
    #Receives the confirmation or denial of the request
    msgServer, trash = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = msgServer.decode()

    if msgFromServer == msgNACK:
        print("ERROR: Server didn't acknowledge request for an unknown reason.")
        return True
    elif msgFromServer != msgACK:
        print("ERROR: " + msgFromServer)
        return True

    #print("server response: " + msgFromServer)  # DEBUG
    clientSocket.close()
    print("Connection with server is closed.")
    return False


def getFileFromServer(serverAddressPort, serverFileName, clientFileName):

    # Verifies if the file exists
    if os.path.exists("./" + clientFileName):
        print("A file with the indicated name already exists on the client.")
        return

    # Sends the request to the server
    UDPClientSocket.sendto((msgGET + " " + serverFileName).encode(), serverAddressPort)

    # Receives the confirmation or denial of the request
    msgServer, trash = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = msgServer.decode().split(" ")

    # Denial handling
    if msgFromServer[0] != msgACK:
        if msgFromServer[0] == msgNACK:
            if msgFromServer[1] == GET_SERVER_MISS_FILE:
                print("The requested file does not exist on server")
            else:
                print("ERROR: Server didn't acknowledge request for an unknown reason. " + msgServer.decode())
        else:
            print("ERROR: Unknown answer from the server. " + msgServer.decode())
        return

    # Accept TCP connection
    connSocket, addr = clientSocket.accept()

    # Receiving from the server and writing to the clientFile
    clientFile = open("./" + clientFileName, "wb")


    fileBuffer = connSocket.recv(bufferSize)  # The file was opened in binary mode, so no need to decode
    while fileBuffer:
        clientFile.write(fileBuffer)
        fileBuffer = connSocket.recv(bufferSize)

    # Closing the socket and closing the file
    connSocket.close()
    clientFile.close()

    print("File download complete: file " + serverFileName +
          " from the server is " + clientFileName + " in the client.")


def putFileInServer(serverAddressPort, serverFileName, clientFileName):
    # Opens the file if it exists
    try:
        clientFile = open("./" + clientFileName, "rb")
    except FileNotFoundError:
        print("The indicated file does not exist on the client.")
        return

    # Sends the request to the server
    UDPClientSocket.sendto((msgPUT + " " + serverFileName).encode(), serverAddressPort)

    # Receives the confirmation or denial of the request
    msgServer, trash = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = msgServer.decode().split(" ")

    # Denial Handling
    if msgFromServer[0] != msgACK:
        if msgFromServer[0] == msgNACK:
            if msgFromServer[1] == PUT_SERVER_EXISTS_FILE:
                print("A file with the indicated name already exists on the server")
            else:
                print("ERROR: Server didn't acknowledge request for an unknown reason. " + msgServer.decode())
                # in case we want to add another exception for protection
        else:
            print("ERROR: Unknown answer from the server. " + msgServer.decode())  # just for protection
        return

    # Accept TCP connection
    connSocket, addr = clientSocket.accept()

    # Send file to the server
    fileBuffer = clientFile.read(bufferSize)  # The file was opened in binary mode, so no need to encode
    while fileBuffer:
        connSocket.send(fileBuffer)
        fileBuffer = clientFile.read(bufferSize)

    # Closing the socket and Closing the file
    connSocket.shutdown(SHUT_RDWR)
    connSocket.close()
    clientFile.close()

    print("File upload complete: file " + clientFileName +
          " from the client is " + serverFileName + " in the server.")


# Check if the module is being run as the main program
# if it is then the program starts here
if __name__ == "__main__":
    main()
