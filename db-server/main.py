from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import constants
import os.path
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

class DBServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = get_path(self)

        #
        # code: 200
        # Connection stablished.
        #
        if (path == ''):
            res = { "response": { "code": 200, "message": "Connected" } }
            response(self, 200, res)

        #
        # code: 200
        # Data from file (also []).
        #
        elif (path == '/files'):
            # Open file to read
            f = open('data.store', 'r')
            
            # List keys
            database = json.load(f) 
            keys = [list(d.keys()) for d in database]
            all_keys = []
            data = []
            for k in keys:
                all_keys += k
            
            # Select distinct
            for k in all_keys:
                if not k in data:
                    data.append(k)
            
            # Send response
            res = { "data": data }
            response(self, 200, res)

        #
        # code: 200
        # Data by ID.
        #
        elif (path.find('/files/') == 0):
            # Get ID
            id = path[7:]
            
            # Open file to read
            f = open('data.store', 'r')
            database = json.load(f)

            # Looking for ID
            data = [d for d in database if id in list(d.keys())]

            # Send response
            res = { "data": data }
            response(self, 200, res)

        #
        # code: 404
        # Resource not found.
        #
        else:
            res = { "error": { "code": 404, "message": "Resource not found" } }
            response(self, 404, res)

    def do_POST(self):
        path = get_path(self)
        
        #
        # code: 201
        # Data added.
        #
        # code: 404
        # Bad format for JSON.
        #
        if (path == '/files'):
            # Get body
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            try:
                entry = json.loads(field_data.decode(constants.ENCODING_FORMAT))
            except:
                res = { "error": { "code": 404, "message": "Bad format for JSON" } }
                response(self, 404, res)
                return

            # Create data.store if it is not exists
            if not os.path.exists('./data.store'):
                f = open('data.store', 'x')
                f.write('[]')
                f.close()
            
            # Get JSON in file to append entries
            f = open('data.store', 'r')
            data = json.load(f)
            if isinstance(entry, list):
                data.append([e for e in entry])
            else:
                data.append(entry)
            
            # Set JSON
            f = open('data.store', 'w')
            json.dump(data, f)
            f.close()

            res = { "data": data }
            response(self, 201, res)
        
        #
        # code: 404
        # Resource not found.
        #
        else:
            res = { "error": { "code": 404, "message": "Resource not found" } }
            response(self, 404, res)


if __name__ == "__main__":
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), DBServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.\n")