# Python 3 server example
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import constants
import requests
import json
#from Crypto.Cipher import AES
#from secrets import token_bytes

class MoisesServer(BaseHTTPRequestHandler):
    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        
        if (path == '/'):
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            body = json.loads(field_data.decode(constants.ENCODING_FORMAT))

            if not 'data_0' in body:
                res = { "error": { "code": 400, "message": "Missing 'data_0' in body" } }
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))
            if not 'data_1' in body:
                res = { "error": { "code": 400, "message": "Missing 'data_1' in body" } }
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))
            if not 'data_2' in body:
                res = { "error": { "code": 400, "message": "Missing 'data_2' in body" } }
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))
            else:
                name = body['name']
                part1 = body['data_0']
                part2 = body['data_1']
                part3 = body['data_2']
                name_encrypted = name

                try:
                    requests.post(
                        constants.GROUP_1_IP+':'+str(constants.NODE_PORT),
                        data=json.dumps({ name_encrypted: part1}),
                        headers={ 'content-type': 'application/json' }
                    )
                    requests.post(
                        constants.GROUP_2_IP+':'+str(constants.NODE_PORT),
                        data=json.dumps({ name_encrypted: part2}),
                        headers={ 'content-type': 'application/json' }
                    )
                    requests.post(
                        constants.GROUP_3_IP+':'+str(constants.NODE_PORT),
                        data=json.dumps({ name_encrypted: part3}),
                        headers={ 'content-type': 'application/json' }
                    )
                    res = { "status": { "code": 202, "message": "Accepted" } }
                    self.send_response(202)
                    self.send_header("content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT)) 
                except requests.exceptions.RequestException as e:
                    res = { "error": { "code": 500, "message": e.response } }
                    self.send_response(404)
                    self.send_header("content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))

        else:
            res = { "error": { "code": 404, "message": "404 Resource Not Found" } }
            self.send_response(404)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))

if __name__ == "__main__":
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), MoisesServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
