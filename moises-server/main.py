# Python 3 server example
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import constants
import requests
import json
import hashlib

class ConvertIRServer(BaseHTTPRequestHandler):
    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        
        if (path == '/'):
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            body = json.loads(field_data.decode(constants.ENCODING_FORMAT))
            if not 'data_0' in body:
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes("Missing 'data_0' in body", constants.ENCODING_FORMAT)) 
            if not 'data_1' in body:
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes("Missing 'data_1' in body", constants.ENCODING_FORMAT)) 
            if not 'data_2' in body:
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes("Missing 'data_2' in body", constants.ENCODING_FORMAT))    
            
            else:
                try:
                    
                    name = body['name']
                    part1 = body['data_0']
                    part2 = body['data_1']
                    part3 = body['data_2']
                    data = {'status': 'recieved'}
                    requests.post(
                        "http://"+constants.GROUP_1+":"+ constants.GROUP_1_PORT,
                        data=json.dumps({ hashlib.sha256(name.encode()).hexdigest(): part1}),
                        headers={ 'content-type': 'application/json' }
                    )
                    requests.post(
                        "http://"+constants.GROUP_2+":"+ constants.GROUP_2_PORT,
                        data=json.dumps({ hashlib.sha256(name.encode()).hexdigest(): part2}),
                        headers={ 'content-type': 'application/json' }
                    )
                    requests.post(
                        "http://"+constants.GROUP_3+":"+ constants.GROUP_3_PORT,
                        data=json.dumps({  hashlib.sha256(name.encode()).hexdigest(): part3}),
                        headers={ 'content-type': 'application/json' }
                    )
                    res = { "data": data }
                    self.send_response(202)
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
