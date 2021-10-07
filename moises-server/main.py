from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import constants
import requests
import json

def to_string(dict):
    return str(dict).replace("'", '"')

def response(server, code, response):
    server.send_response(code)
    server.send_header("content-type", "application/json")
    server.end_headers()
    server.wfile.write(bytes(to_string(response), constants.ENCODING_FORMAT))  

def get_path(server):
    url = urlparse(server.path)
    path = url.path
    path = path[:-1] if path[-1] == '/' else path
    return path

class MoisesServer(BaseHTTPRequestHandler):
    def do_POST(self):
        path = get_path(self)
        
        #
        # code: 400
        # For any missing parameter.
        #
        # code: 202
        # Data to add sent to DB Server.
        #
        # code: 500
        # DB Server Connection refused.
        #
        if (path == '/files'):
            # Get body
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            
            # Get body JSON
            try:
                body = json.loads(field_data.decode(constants.ENCODING_FORMAT))
            except:
                res = { "error": { "code": 400, "message": "Bad format for JSON" } }
                response(self, 400, res)
                return

            # Check parameters
            if not 'name' in body:
                res = { "error": { "code": 400, "message": "Missing [name] in body" } }
                response(self, 400, res)
                return
            
            elif not 'data_0' in body:
                res = { "error": { "code": 400, "message": "Missing [data_0] in body" } }
                response(self, 400, res)
                return
            
            elif not 'data_1' in body:
                res = { "error": { "code": 400, "message": "Missing [data_1] in body" } }
                response(self, 400, res)
                return

            elif not 'data_2' in body:
                res = { "error": { "code": 400, "message": "Missing [data_2] in body" } }
                response(self, 400, res)
                return
            
            else:
                # Get parameters
                name = body['name']
                part0 = body['data_0']
                part1 = body['data_1']
                part2 = body['data_2']
                name_encrypted = name # TODO: encrypt via AES

                # Requests for DB Server
                try:
                    requests.post(
                        f'{constants.GROUP_1_IP}:{constants.NODE_PORT}/files',
                        data=json.dumps({ name_encrypted: part0 }),
                        headers={ 'content-type': 'application/json' }
                    )
                    requests.post(
                        f'{constants.GROUP_2_IP}:{constants.NODE_PORT}/files',
                        data=json.dumps({ name_encrypted: part1 }),
                        headers={ 'content-type': 'application/json' }
                    )
                    requests.post(
                        f'{constants.GROUP_3_IP}:{constants.NODE_PORT}/files',
                        data=json.dumps({ name_encrypted: part2 }),
                        headers={ 'content-type': 'application/json' }
                    )
                    res = { "status": { "code": 202, "message": "Accepted" } }
                    response(self, 202, res) 
                except requests.exceptions.RequestException as e:
                    res = { "error": { "code": 500, "message": "Internal Error: DB Server Connection Refused" } }
                    response(self, 500, res)
        
        #
        # code: 404
        # Resource not found.
        #
        else:
            res = { "error": { "code": 404, "message": "Resource not found" } }
            response(self, 404, res)

if __name__ == "__main__":
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), MoisesServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
