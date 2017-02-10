from socket import *
import hashlib
badRequestResponse = "HTTP/1.0 400 Bad Request"

def handleRequest(connectionSocket):
    #RECEIVE THE REQUEST
    requestBytes = b''
    while True:
        requestBytes += connectionSocket.recv(2048)
        if requestBytes.decode()[-4:] == "\r\n\r\n": break
    request = requestBytes.decode()
    
    #SPLIT THE REQUEST
    splitRequest = request.split(maxsplit=3)
    try:
        method = splitRequest[0]
        URL = splitRequest[1]
        httpVersion = splitRequest[2]
    except Exception as e:
        connectionSocket.send(badRequestResponse.encode())
        connectionSocket.close()
        return

    #PARCE THE URL
    try:
        splitURL = URL.split('/', maxsplit=3)
        serverName = splitURL[2]
        pathName = splitURL[3]
    except Exception as e:
        connectionSocket.send(badRequestResponse.encode())
        connectionSocket.close()
        return

    #GRAB HEADERS IF ANY
    try:
        headers = splitRequest[3]
    except Exception as e:
        headers = ""

    #FORMAT THE REQUEST FOR THE SERVER
    request = "GET /" + pathName + " " + httpVersion + "\r\n"
    request += "Host: " + serverName + "\r\n"
    request += "Conection: close" + "\r\n"
    request += headers + "\r\n\r\n"

    print(request)

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

