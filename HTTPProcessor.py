
HTTP_OK = "HTTP/1.0 200 OK"
HTTP_OK1 = "HTTP/1.1 200 OK"

class HTTPRequest:
    hasError = False
    errorMessage = ""
    
    method = ""
    URL = ""
    httpVersion = ""
    serverName = ""
    pathName = ""
    headers = ""
    relativeFormat = ""


class HTTPResponse:
    responseStatus = ""
    response = ""


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
        badRequest.hasError = True
        badRequest.errorMessage = "Was not abble to interpret request:\n" + requestString
        return badRequest

    #CHECK ABSOLUTE FORMAT
    if (request.URL[:7] != "http://") & (request.URL[:8] != "https://"):
        badRequest = HTTPRequest()
        badRequest.hasError = True
        badRequest.errorMessage = "Request was not in absolute URI format\n"
        return badRequest

    #PARCE THE URL
    try:
        splitURL = request.URL.split('/', maxsplit=3)
        request.serverName = splitURL[2]
        request.pathName = splitURL[3]
    except Exception as e:
        badRequest = HTTPRequest()
        badRequest.hasError = True
        badRequest.errorMessage = "Was unable to parse URL"
        return badRequest
    
    #GRAB HEADERS IF ANY
    try:
        request.headers = splitRequest[3]
    except Exception as e:
        request.headers = ""
    
    #FORMAT THE REQUEST FOR THE SERVER
    relativeFormat = "GET /" + request.pathName + " " + request.httpVersion + "\r\n"
    relativeFormat += "Host: " + request.serverName + "\r\n"
    relativeFormat += request.headers + "\r\n"
    relativeFormat += "Conection: close" + "\r\n\r\n"

    request.relativeFormat = relativeFormat

    #RETURN THE FORMATED REQUEST
    return request



def processResponse(responseString):
    
    response = HTTPResponse()
    
    #SPLIT THE RESPONSE FOR RESPONSE STATUS
    responseStatus = responseString.split('\r\n', maxsplit=1)[0]
    response.responseStatus = responseStatus
    
    #WHOLE RESPONSE
    response.response = responseString
    
    #RETURN THE RESPONSE
    return response






















