# Python 3 server example
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import constants
import os
import json

class DBServer(BaseHTTPRequestHandler):

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        if (path == '/'):
            f = open('data.store', 'r')
            data = json.load(f)
            res = { "data": data }
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))    

        elif (path == '/data'):
            if (len(query) == 0 or not 'id' in query):
                res = { "error": { "code": 400, "message": "Missing 'id' as query parameter" } }
                self.send_response(400)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))
            else:
                f = open('data.store', 'r')
                datalist = json.load(f)

                data = [d for d in datalist if d['id'] == query['id'][0]]

                res = { "data": data }
                self.send_response(200)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))
        
        else:
            res = { "error": { "code": 404, "message": "404 Resource Not Found" } }
            self.send_response(404)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(res), constants.ENCODING_FORMAT))

    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)
        
        if (path == '/'):
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            
            try:
                f = open('data.store', 'x')
                print('data.store created')
                f.write('[]')
                f.close()
            except:
                print('data.store modified')
            
            f = open('data.store', 'r')
            data = json.load(f)
            entry = json.loads(field_data.decode(constants.ENCODING_FORMAT))
            if isinstance(entry, list):
                for e in entry:
                    data.append(e)
            else:
                data.append(entry)
            f.close()

            f = open('data.store', 'w')
            json.dump(data, f)

            res = { "data": data }
            self.send_response(201)
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
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), DBServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.\n")