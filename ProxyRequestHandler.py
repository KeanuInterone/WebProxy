from socket import *
import hashlib
import HTTPProcessor

GOOD_RESPONSE = "HTTP/1.0 200 OK"
FOUND_MALWARE_HTML = "<h1>Sight was blocked, maleware was detected!</h1>"
METHOD_NOT_IMPLEMENTED = "HTTP/1.0 501 NOT_IMPLEMENTED"
BAD_REQUEST= "HTTP/1.0 400 BAD_REQUEST"


def handleRequest(connectionSocket):
    
    #RECEIVE THE REQUEST
    requestBytes = b''
    while True:
        requestBytes += connectionSocket.recv(2048)
        if requestBytes.decode()[-4:] == "\r\n\r\n": break
    requestString = requestBytes.decode()
    print(requestString)

    #PROCESS THE CLIENT REQUEST
    request = HTTPProcessor.processRequest(requestString)

    if (request.hasError == False) & (request.method != "GET"):
        errorResponse = METHOD_NOT_IMPLEMENTED + "\r\n\r\n" + request.method + " request is not implemented in this proxy"
        connectionSocket.send(errorResponse.encode())
        connectionSocket.close()
        return
    if request.hasError:
        errorResponse = BAD_REQUEST + "\r\n\r\n" + request.errorMessage
        connectionSocket.send(errorResponse.encode())
        connectionSocket.close()
        return

    #SEND REQUEST TO THE SERVER
    try:
        httpSocket = socket(AF_INET, SOCK_STREAM)
        httpSocket.connect((request.serverName, 80))
        httpSocket.send(request.relativeFormat.encode())
    except Exception as e:
        connectionSocket.send(BAD_REQUEST.encode())
        connectionSocket.close()
        return

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
        # IF ERROR RESPONSE FROM SERVER, SEND TO CLIENT
        connectionSocket.send(serverResponse.response.encode())
        connectionSocket.close()
        return

    #CONVERT THE TEXT INTO A MD5
    fileMD5 = hashlib.md5(response).digest()

    #CONNECT TO  hash.cymru.com AND SEND MD5
    cymruSocket = socket(AF_INET, SOCK_STREAM)
    cymruSocket.connect(("hash.cymru.com", 43))
    cymruSocket.send(fileMD5)

    #GET THE RESPONSE BACK FROM CYMRU
    cymruResponse = b''
    while True:
        data = httpSocket.recv(2048)
        if not data: break
        cymruResponse += data
    print("cyrmu response: " + cymruResponse.decode())

    if not cymruResponse:
        #STEP 4: SEND RESPONSE BACK TO CLIENT
        connectionSocket.send(response)
        connectionSocket.close()
        return
    else:
        foundMalwareResponse = GOOD_RESPONSE + "\r\n\r\n" + FOUND_MALWARE_HTML
        connectionSocket.send(foundMalwareResponse.encode())
        connectionSocket.close()
        return





















