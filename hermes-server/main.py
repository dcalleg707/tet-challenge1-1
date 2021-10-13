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

def check_ips(ip_list):
    new_ip = ""
    for ip in ip_list:
        try:
            test = requests.get(f'{ip}:{constants.NODE_PORT}/', timeout=0.6)
            new_ip = ip
            break
        except:
            print(f'DB Server {ip} connection failed!')
    
    if new_ip != '':
        return new_ip
    else:
        raise requests.exceptions.RequestException

class HermesServer(BaseHTTPRequestHandler):
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
        # Files were found and sent.
        #
        # code: 500
        # DB Server Connection refused.
        #
        elif (path == '/files'):
            try:
                # Get available ip from any GROUP
                ip_to_ask = check_ips(constants.GROUP_1_IP + constants.GROUP_2_IP + constants.GROUP_3_IP)
                part0 = requests.get(f'{ip_to_ask}:{constants.NODE_PORT}/files')

                data = json.loads(part0.text)['data']
                data = [d for d in data]
                
                # Send response
                res = { "data": data }
                response(self, 200, res)
            
            except requests.exceptions.RequestException as e:
                res = { "error": { "code": 500, "message": "Internal Error: DB Server Connection Refused" } }
                response(self, 500, res)
        
        #
        # code: 200
        # File was found and sent.
        #
        # code: 404
        # File does not exist in DB Server.
        #
        # code: 500
        # DB Server Connection refused.
        #
        elif (path.find('/files/') == 0):
            # Get ID
            id = path[7:]
            
            try:
                # Connect to DB Server and read data
                ip_part1 = check_ips(constants.GROUP_1_IP)
                ip_part2 = check_ips(constants.GROUP_2_IP)
                ip_part3 = check_ips(constants.GROUP_3_IP)

                part0 = requests.get(f'{ip_part1}:{constants.NODE_PORT}/files/{id}')
                part1 = requests.get(f'{ip_part2}:{constants.NODE_PORT}/files/{id}')
                part2 = requests.get(f'{ip_part3}:{constants.NODE_PORT}/files/{id}')
                data = json.loads(part0.text)['data'] + json.loads(part1.text)['data'] + json.loads(part2.text)['data']

                # Send response
                if (len(data) != 0):
                    res = { "data": data }
                    response(self, 200, res)
                else:
                    res = { "error": { "code": 404, "message": f"Data not found with id: {id}" } }
                    response(self, 404, res)
                
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
    webServer = HTTPServer((constants.IP_SERVER, constants.PORT), HermesServer)
    print("Server started http://%s:%s" % (constants.IP_SERVER, constants.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
