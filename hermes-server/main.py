# Python 3 server example
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import constants
import requests
import json

def to_string(dict):
    return str(dict).replace("'", '"')

class HermesServer(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        for k in query.keys(): # Query string values can be lists. We get the first value only
            query[k] = query[k][0]
        
        if (path == '/'):
            try:
                if ('id' in query):
                    part0 = requests.get(f'{constants.GROUP_1_IP}:{constants.NODE_PORT}/data?id={query["id"]}')
                    data = json.loads(part0.text)['data']
                else:
                    part0 = requests.get(f'{constants.GROUP_1_IP}:{constants.NODE_PORT}')
                    data = json.loads(part0.text)['data']
                    data = [d for d in data] # TODO: decode here
                
                if len(data) != 0:
                    res = { "data": data }
                    self.send_response(200)
                    self.send_header("content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(bytes(to_string(res), constants.ENCODING_FORMAT)) 
                else:
                    res = { "error": { "code": 404, "message": f"No data was found with id {query['id']}"} }
                    self.send_response(404)
                    self.send_header("content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(bytes(to_string(res), constants.ENCODING_FORMAT)) 
            except requests.exceptions.RequestException as e:
                res = { "error": { "code": 500, "message": e.response } }
                self.send_response(500)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(to_string(res), constants.ENCODING_FORMAT))

        else:
            self.send_response(404)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("404 Error: Resource %s not found" % path, constants.ENCODING_FORMAT))

if __name__ == "__main__":
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), HermesServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
