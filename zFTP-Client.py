#print("Hello Client World!")

from socket import *
import sys  #needed to access the command-line arguments

serverName = "localhost"            # server name
serverPort = 12000                  # socket server port number
sockBuffer = 1024                   # socket buffer size
serverAddressPort   = ("127.0.0.1", 20001) #for UDP

msgCLOSE = "close"
msgOPEN = "open"
msgGET = "get"
msgPUT = "put"
#msgACK = "ACK"
#msgOK = "OK"
#msgSTART = "START"

def main():
    UDPClientSocket = socket(AF_INET, SOCK_DGRAM)

    #parte do sebas

    #clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    #clientSocket.connect((serverName, serverPort))   # open TCP connection
    len_args = len(sys.argv)       #get number of arguments
    if (len_args != 3):
        print ("wrong number of arguments please put only the server name and the UDP Port so the server can recieve commands")
    else:
        print("server port" , sys.argv[1]) #after that check if the port is valid

    print("Hello Client World!")

    #parte do goncalo
    while True:
        line = input("-> ")
        arrLine = line.split(" ")
        cmd = arrLine[0]
        numArg = len(arrLine) - 1

        if cmd == msgOPEN:
            if numArg != 1:
                print("Invalid number of arguments.")
            else:
                numPort = int(arrLine[1])
                if numPort < 1024 or numPort > 65535:
                    print("Invalid Port Number.")
                else:
                    openConection(UDPClientSocket, arrLine[1])
            # ...
        elif cmd == msgGET:
            if numArg != 2:
                print("Invalid number of arguments.")
            else:
                #get_command(clientSocket, socketUDP, serverName, filename)
        # ...

        elif cmd == msgPUT:
            if numArg != 2:
                print("Invalid number of arguments.")
            else:
                filename = arrLine[1]
                #put_command(clientSocket, socketUDP, serverName, filename)
        # ...

        elif cmd == msgCLOSE:
            clientSocket.send(msgCLOSE.encode())
            clientSocket.close()
            break

        else:
            print("Command not found")

def openConection(UDPClientSocket, port):
    UDPClientSocket.sendto(port.encode(), serverAddressPort)

if __name__ == "__main__":  #check if the module is being run as the main program
    main()