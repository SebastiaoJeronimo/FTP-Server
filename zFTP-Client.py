from socket import *
import sys  #needed to access the command-line arguments 

serverName = "localhost"            # server name
serverPort = 12000                  # socket server port number
sockBuffer = 2048                   # socket buffer size

def main():
    #clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket
    #clientSocket.connect((serverName, serverPort))   # open TCP connection
    len_args = len(sys.argv)       #get number of arguments
    if (len_args != 3):
        print ("wrong number of arguments please put only the server name and the UDP Port so the server can recieve commands")
    else:
        print("server port" , sys.argv[1]) #after that check if the port is valid

    print("Hello Client World!")


if __name__ == "__main__":  #check if the module is being run as the main program
    main()