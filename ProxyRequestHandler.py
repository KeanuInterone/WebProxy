from socket import *


def handleRequest(connectionSocket):
    #RECEIVE THE REQUEST
    requestBytes = b''
    while True:
        requestBytes += connectionSocket.recv(2048)
        if requestBytes.decode()[-4:] == "\r\n\r\n": break
    request = requestBytes.decode()


    #CHECK AND FORMAT THE REQUEST
    requestLine = requestBytes.split()

    if len(requestLine) < 3:
        print("we got a bad request")
    if requestLine[0].decode() != "GET":
        print("method not implemented")

    method =  requestLine[0].decode()
    url = requestLine[1].decode()
    version = requestLine[2].decode()

    urlArray = url.split('/', maxsplit=3)
    host = urlArray[2]
    path = urlArray[3]

    request = "GET /" + path + " " + version + "\r\n" + "Host: " + host + "\r\n" + "Conection: close" + "\r\n\r\n"
    print(request)
    serverName = host


    #SEND REQUEST TO THE SERVER
    httpSocket = socket(AF_INET, SOCK_STREAM)
    httpSocket.connect((serverName, 80))
    httpSocket.send(request.encode())

    #RECEIVE THE RESPONSE FROM THE SERVER
    response = b''
    while True:
        data = httpSocket.recv(2048)
        if not data: break
        response += data


    #STEP 4: SEND RESPONSE BACK TO CLIENT
    connectionSocket.send(response)
    connectionSocket.close()
