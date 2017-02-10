
BAD_REQUEST = "BAD_REQUEST"
HTTP_OK = "HTTP/1.0 200 OK"
HTTP_OK1 = "HTTP/1.1 200 OK"

class HTTPRequest:
    flag = ""
    method = ""
    URL = ""
    httpVersion = ""
    serverName = ""
    pathName = ""
    headers = ""
    relativeFormat = ""


def processRequest(requestString):
    
    request = HTTPRequest()
    
    #SPLIT THE REQUEST
    splitRequest = requestString.split(maxsplit=3)
    try:
        request.method = splitRequest[0]
        request.URL = splitRequest[1]
        request.httpVersion = splitRequest[2]
    except Exception as e:
        badRequest = HTTPRequest()
        badRequest.flag = BAD_REQUEST
        return badRequest
    
    #PARCE THE URL
    try:
        splitURL = request.URL.split('/', maxsplit=3)
        request.serverName = splitURL[2]
        request.pathName = splitURL[3]
    except Exception as e:
        badRequest = HTTPRequest()
        badRequest.flag = BAD_REQUEST
        return badRequest
    
    #GRAB HEADERS IF ANY
    try:
        request.headers = splitRequest[3]
    except Exception as e:
        request.headers = ""
    
    #FORMAT THE REQUEST FOR THE SERVER
    relativeFormat = "GET /" + request.pathName + " " + request.httpVersion + "\r\n"
    relativeFormat += "Host: " + request.serverName + "\r\n"
    relativeFormat += "Conection: close" + "\r\n"
    relativeFormat += request. headers + "\r\n\r\n"

    request.relativeFormat = relativeFormat

    #RETURN THE FORMATED REQUEST
    return request


class HTTPResponse:
    responseStatus = ""
    response = ""

def processResponse(responseString):
    
    response = HTTPResponse()
    
    #SPLIT THE RESPONSE FOR RESPONSE STATUS
    responseStatus = responseString.split('\r\n', maxsplit=1)
    print(responseStatus[0])
    response.responseStatus = responseStatus
    
    #WHOLE RESPONSE
    response.response = responseString
    
    #RETURN THE RESPONSE
    return response






















