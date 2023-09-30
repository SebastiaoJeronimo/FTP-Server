# print("Hello Client World!")
import os
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

msgACK = "ACK"
msgNACK = "NACK"

PUT_ERROR_FILE_CLIENT = "2"
GET_ERROR_FILE_SERVER = "3"
# msgOK = "OK"
# msgSTART = "START"


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
        arrLine = line.split(" ")
        cmd = arrLine[0]
        numArg = len(arrLine) - 1  # Don't count the name of the file that has the code to run

        if cmd == msgOPEN:
            if numArg != 1:
                print("Invalid number of arguments.")
            else:
                numPort = int(arrLine[1])
                if numPort < 1024 or numPort > 65535:
                    print("Invalid Port Number.")
                else:
                    openConnection(arrLine[1])

        elif cmd == msgGET:
            if numArg != 2:
                print("Invalid number of arguments.")
            else:
                serverFile = arrLine[1]
                clientFile = arrLine[2]
                getFileFromServer(serverFile, clientFile)

        elif cmd == msgPUT:
            if numArg != 2:
                print("Invalid number of arguments.")
            else:
                clientFile = arrLine[1]
                serverFile = arrLine[2]
                putFileInServer(serverFile, clientFile)

        elif cmd == msgCLOSE:
            closeConnection()
            break  # To stop the loop

        else:
            print("No Command: " + cmd)


# Tell Server to open TCP Connection
def openConnection(port):
    UDPClientSocket.sendto((msgOPEN + "" + port).encode(), serverAddressPort)
    msgFromServer = (UDPClientSocket.recvfrom(bufferSize)).decode()
    if msgFromServer != msgACK:
        print("ERROR: Server didn't acknowledge request for an unknown reason.")


# Close the TCP Connection and tell server to do the same
def closeConnection():
    UDPClientSocket.sendto(msgCLOSE.encode(), serverAddressPort)
    msgFromServer = (UDPClientSocket.recvfrom(bufferSize)).decode()
    if msgFromServer != msgACK:
        print("ERROR: Server didn't acknowledge request for an unknown reason.")
    else:
        clientSocket.close()


def getFileFromServer(serverFileName, clientFileName):
    if os.path.exists("./clientFiles/" + clientFileName):
        print("A file with the indicated name already exists on the client.")
        return

    UDPClientSocket.sendto((msgGET + " " + serverFileName).encode(), serverAddressPort)
    msgFromServer = ((UDPClientSocket.recvfrom(bufferSize)).decode()).split(" ")

    if msgFromServer[1] == msgNACK:
        if msgFromServer[2] == GET_ERROR_FILE_SERVER:
            print("The requested file does not exist on server")
        else:
            print("ERROR: Server didn't acknowledge request for an unknown reason.")

        return

    clientFile = open("./clientFiles/" + clientFileName, "wb")

    fileBuffer = clientSocket.recv(bufferSize)
    while fileBuffer:
        clientFile.write(fileBuffer)
        fileBuffer = clientSocket.recv(bufferSize)

    """   #nao apagues isto ate termos a certeza
    clientSocket.close() #????
    """
    clientFile.close()

def putFileInServer(serverFileName, clientFileName): # TODO
    print("hello")


# Check if the module is being run as the main program
# if it is then the program starts here
if __name__ == "__main__":
    main()
