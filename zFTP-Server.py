import sys  #needed to access the command-line arguments
from socket import *

# socket buffer size
bufferSize = 1024

global serverAddressPort
global TCPSocket
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
        print ("wrong number of arguments please put only the UDP Port so the server can recieve commands")
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


    #TODO daqui para baixo foi copiado do client
    while True:
        line = UDPSocket.recvfrom(bufferSize)
        arrLine = line.decode().split(" ")  # Array with the input
        cmd = arrLine[0]
        numArg = len(arrLine) - 1  # Don't count the name of the command

        if cmd == msgOPEN:
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



if __name__ == "__main__":  #check if the module is being run as the main program
    main()