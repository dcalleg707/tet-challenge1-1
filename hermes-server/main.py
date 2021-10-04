# Python 3 server example
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import constants
import json
import hashlib
import requests

class ConvertIRServer(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        for k in query.keys(): # Query string values can be lists. We get the first value only
            query[k] = query[k][0]
        
        if (path == '/'):
            try:
                data =[]
                if('id' in query):
                    id = hashlib.sha256(query['id'].encode()).hexdigest()
                    part1 = requests.get('http://'+constants.GROUP_1+':'+constants.GROUP_1_PORT+'/data?id='+id).text
                    part2 = requests.get('http://'+constants.GROUP_2+':'+constants.GROUP_2_PORT+'/data?id='+id).text
                    part3 = requests.get('http://'+constants.GROUP_3+':'+constants.GROUP_3_PORT+'/data?id='+id).text
                    data = [part1, part2, part3]
                else:
                    part1 = requests.get('http://'+constants.GROUP_1+':'+constants.GROUP_1_PORT).text
                    part2 = requests.get('http://'+constants.GROUP_2+':'+constants.GROUP_2_PORT).text
                    part3 = requests.get('http://'+constants.GROUP_3+':'+constants.GROUP_3_PORT).text
                    data = [part1, part2, part3]

                res = { "data": data}
                self.send_response(200)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT)) 
            except:
                res = { "error": { "code": 404, "message": "404 Resource Not Found" } }
                self.send_response(404)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))
        
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

if __name__ == "__main__":
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), ConvertIRServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
