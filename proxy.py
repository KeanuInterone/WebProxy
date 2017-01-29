from socket import *

#this is the new branch
#this is a chanch in master

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

    
#STEP 1: RECIEVE THE REQUEST
connectionSocket, address = serverSocket.accept()
requestBytes = b''
while True:
    requestBytes += connectionSocket.recv(2048)
    if requestBytes.decode()[-4:] == "\r\n\r\n": break
request = requestBytes.decode()


#STEP 2: CHECK AND FORMAT THE REQUEST

### working code
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


#STEP 3: SEND REQUEST TO THE SERVER
httpSocket = socket(AF_INET, SOCK_STREAM)
httpSocket.connect((serverName, 80))
httpSocket.send(request.encode())
response = b''
while True:
    data = httpSocket.recv(2048)
    if not data: break
    response += data


#STEP 4: SEND RESPONSE BACK TO CLIENT
connectionSocket.send(response)
connectionSocket.close()

