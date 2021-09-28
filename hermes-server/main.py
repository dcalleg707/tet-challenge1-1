# Python 3 server example
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import constants

class ConvertIRServer(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        for k in query.keys(): # Query string values can be lists. We get the first value only
            query[k] = query[k][0]
        
        if (path == '/'):
            if len(query) < 2 or not ('value' in query and 'actualIrType' in query and 'newIrType' in query):
                self.send_response(400)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes("Missing arguments on query string (value, actualIrType, newIrType)", constants.ENCODING_FORMAT))
            elif verify_arguments(query['value'], query['actualIrType'], query['newIrType']) < 0:
                self.send_response(400)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes("Incorrect values: some query params has 'str' instead of 'float' or vice versa", constants.ENCODING_FORMAT))
            else:
                value = float(query['value'])
                actualIrType = str(query['actualIrType'])
                newIrType = str(query['newIrType'])
                res = change_ir(value, actualIrType, newIrType)
                res = str(round(res, 2))
                self.send_response(200)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes(res, constants.ENCODING_FORMAT))
        
        elif (path == '/ping'):
            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Connection established", constants.ENCODING_FORMAT))
        
        elif (path == '/help'):
            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Welcome to Interest Rate Conversion Server!\\nAvailable resources: /, /help, /ping\n\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("RESOURCES\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("/ (usage: /?value=FLOAT&actualIrType=STR&newIrType=STR)\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("    This resource changes interest rate type for another one.\n\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("/help (usage: /help)\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("    This resource explains all available server interactions and resources.\n\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("/ping (usage: /ping)\n", constants.ENCODING_FORMAT))
            self.wfile.write(bytes("    This resource helps to test if server connection was established.\n\n", constants.ENCODING_FORMAT))

        else:
            self.send_response(404)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("404 Error: Resource %s not found" % path, constants.ENCODING_FORMAT))

def verify_arguments(val, actual_irt, new_irt):
    try:
        float(val)
        str(actual_irt)
        str(new_irt)
    except ValueError:
        return -1
    return 0

def change_ir(value, actual_irt, new_irt):
    #value = float(remote_command[1])
    #actual_irt = remote_command[2]
    #new_irt = remote_command[3]

    if(actual_irt == new_irt):
        return value
    elif(actual_irt == "EM" and new_irt == "EA"):
        return (((1+(value/100))**12) - 1) * 100
    elif(actual_irt == "EM" and new_irt == "NMV"):
        return value*12
    elif(actual_irt == "EM" and new_irt == "NAV"):
        return (((1+(value/100))**12)-1)*100
    elif(actual_irt == "EA" and new_irt == "EM"):
        return (((1+(value/100))**(1/12)) - 1) * 100
    elif (actual_irt == "EA" and new_irt == "NMV"):
        return (((1+(value/100))**(1/12)) - 1) * 12 * 100
    elif (actual_irt == "EA" and new_irt == "NAV"):
        return value
    elif (actual_irt == "NMV" and new_irt == "EM"):
        return value/12
    elif (actual_irt == "NMV" and new_irt == "EA"):
        return (((((value/100)/12) + 1)**12) - 1) * 100
    elif (actual_irt == "NMV" and new_irt == "NAV"):
        return (((((value/100)/12) + 1)**12) - 1) * 100
    elif (actual_irt == "NAV" and new_irt == "EM"):
        return ((((value/100) + 1)**(1/12)) - 1) * 100
    elif (actual_irt == "NAV" and new_irt == "EA"):
        return value
    elif (actual_irt == "NAV" and new_irt == "NMV"):
        return ((((value/100) + 1)**(1/12)) - 1) * 12 * 100

if __name__ == "__main__":
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), ConvertIRServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")