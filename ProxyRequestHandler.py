from socket import *
import hashlib
import HTTPProcessor



badRequestResponse = "HTTP/1.0 400 Bad Request"
mneResponse = "mehtod not implemented"
#BAD_REQUEST = "BAD_REQUEST"
MEHTOD_NOT_IMPLEMENTED = "METHOD_NOT_IMPLEMENTED"

def handleRequest(connectionSocket):
    #RECEIVE THE REQUEST
    requestBytes = b''
    while True:
        requestBytes += connectionSocket.recv(2048)
        if requestBytes.decode()[-4:] == "\r\n\r\n": break
    requestString = requestBytes.decode()

    #PROCESS THE CLIENT REQUEST
    request = HTTPProcessor.processRequest(requestString)

    if request.flag == HTTPProcessor.BAD_REQUEST:
        connectionSocket.send(badRequestResponse.encode())
        connectionSocket.close()
        return
    if request.method != "GET":
        connectionSocket.send(mneResponse.encode())
        connectionSocket.close()
        return

    print(request.relativeFormat)

    #SEND REQUEST TO THE SERVER
    httpSocket = socket(AF_INET, SOCK_STREAM)
    httpSocket.connect((request.serverName, 80))
    httpSocket.send(request.relativeFormat.encode())

    #RECEIVE THE RESPONSE FROM THE SERVER
    response = b''
    while True:
        data = httpSocket.recv(2048)
        if not data: break
        response += data

    #PROCESS THE SERVER RESPONSE
    serverResponse = HTTPProcessor.processResponse(response.decode("utf-8", "replace"))

    #CHECK TO SEE IF RESPONSE WAS GOOD
    if (serverResponse.responseStatus != HTTPProcessor.HTTP_OK) & (serverResponse.responseStatus != HTTPProcessor.HTTP_OK1):
        connectionSocket.send(badRequestResponse.encode())
        connectionSocket.close()
        return

    #CONVERT THE TEXT INTO A MD5
    fileMD5 = hashlib.md5(response).digest()

    #CONNECT TO  hash.cymru.com AND SEND MD5
    cymruSocket = socket(AF_INET, SOCK_STREAM)
    cymruSocket.connect(("hash.cymru.com", 43))
    print("connected to the cymru server")
    #cymruRequest = "begin\r\n" + fileMD5.decode() + "\r\nend\r\n"
    cymruSocket.send(fileMD5)
    #print("sent " + fileMD5.decode() + " to the cymru server")

    #GET THE RESPONSE BACK FROM CYMRU
    cymruResponse = b''
    while True:
        data = httpSocket.recv(2048)
        if not data: break
        cymruResponse += data
    print("cyrmu response: " + cymruResponse.decode())

    #STEP 4: SEND RESPONSE BACK TO CLIENT
    connectionSocket.send(response)
    connectionSocket.close()

