from socket import *
import ProxyRequestHandler
from multiprocessing import Process

while True:
    serverPortString = input('Select a port number: ')
    try:
        serverPort = int(serverPortString)
        break
    except Exception as e:
        print("Not an aceptable port number")


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to use")


while True:
    #STEP 1: RECIEVE THE REQUEST
    connectionSocket, address = serverSocket.accept()

    #START A NEW PROCESS FOR THE REQUEST
    procces = Process(target=ProxyRequestHandler.handleRequest, args=(connectionSocket,))
    procces.start()
    connectionSocket.close()
