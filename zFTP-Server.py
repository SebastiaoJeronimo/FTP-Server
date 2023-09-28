import sys  #needed to access the command-line arguments

localIP      = "127.0.0.1"
localPort    = 20001
bufferSize   = 1024

def main():

    print("Hello Server World!")

    len_args = len(sys.argv)       #get number of arguments
    if (len_args != 2):
        print ("wrong number of arguments please put only the UDP Port so the server can recieve commands")
    else:
        print("server port" , sys.argv[1]) #after that check if the port is valid
    print("Number of arguments: ",len_args-1)
    print("Argument list: ")
    
    for i in range(1, len_args):    #list all arguments
        print(str(sys.argv[i]))


if __name__ == "__main__":  #check if the module is being run as the main program
    main()