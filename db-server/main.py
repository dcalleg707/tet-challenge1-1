# Python 3 server example
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

        if (path == '/files'):
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

        elif (path.find('/files/') == 0):
            # Get ID
            id = path[7:]
            
            # Open file to read
            f = open('data.store', 'r')
            database = json.load(f)

            # Looking for ID
            data = [d for d in database if id in list(d.keys())]

            # Send response
            if (len(data) != 0):
                res = { "data": data }
                response(self, 200, res)
            else:
                res = { "error": { "code": 404, "message": f"Data not found with id: {id}" } }
                response(self, 404, res)

        else:
            res = { "error": { "code": 404, "message": "Resource not found" } }
            response(self, 404, res)

    def do_POST(self):
        path = get_path(self)
        
        if (path == '/files'):
            # Get body
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            entry = json.loads(field_data.decode(constants.ENCODING_FORMAT))

            # Create data.store if it is not exists
            if not os.path.exists('data.store'):
                f = open('data.store', 'x')
                f.write('[]')
                f.close()
            
            # Get JSON in file to append entries
            f = open('data.store', 'r+')
            data = json.load(f)
            if isinstance(entry, list):
                data.append([e for e in entry])
            else:
                data.append(entry)
            
            # Set JSON
            json.dump(data, f)
            f.close()

            res = { "data": data }
            response(self, 201, res)

        else:
            res = { "error": { "code": 404, "message": "404 Resource Not Found" } }
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