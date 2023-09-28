#print("Hello Client World!")

from socket import *
import sys  #needed to access the command-line arguments 

serverName = "localhost"            # server name
serverPort = 12000                  # socket server port number
sockBuffer = 2048                   # socket buffer size

msgCLOSE = "close"
msgOPEN = "open"
msgGET = "get"
msgPUT = "put"
#msgACK = "ACK"
#msgOK = "OK"
#msgSTART = "START"

def main():
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    clientSocket.connect((serverName, serverPort))   # open TCP connection

    while True:
        line = input("-> ")
        arrLine = line.split(" ")
        cmd = arrLine[0]
        numArg = len(arrLine)

        cmd = 'change me'#TODO change

        if cmd == msgOPEN:
            if numArg != 1:
                print("Invalid number of arguments.")
            else:
                #open
            # ...
        elif cmd == msgGET:
            if numArg != 2:
                #print("Invalid arguments")
            else:
                get_command(clientSocket, socketUDP, serverName, filename)
        # ...

        elif cmd == msgPUT:
            if numArg != 2:
                #print("Invalid arguments")
            else:
                filename = cmdLine[1]
                put_command(clientSocket, socketUDP, serverName, filename)
        # ...

        elif cmd == msgCLOSE:
            if numArg != 1:
                #print error
            clientSocket.send(msgQUIT.encode())
            clientSocket.close()
            break

        else:
            print("Command not found")