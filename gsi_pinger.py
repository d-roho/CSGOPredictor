def pingerfunc():

    from http.server import BaseHTTPRequestHandler, HTTPServer
    import time
    import json
    global snapshot
    snapshot = None

    class GSIServer(HTTPServer):
        def __init__(self, server_address, token, RequestHandler):
            self.auth_token = token
            
            super(GSIServer, self).__init__(server_address, RequestHandler)

            
    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            global snapshot
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode('utf-8')
            payload = json.loads(body)

            # Ignore unauthenticated payloads
            if not self.authenticate_payload(payload):
                return None
            
            snapshot = payload
            exit()
            

            self.send_header('Content-type', 'text/html')
            self.send_response(200)
            self.end_headers()
            

        def authenticate_payload(self, payload):
            if 'auth' in payload and 'token' in payload['auth']:
                return payload['auth']['token'] == server.auth_token
            else:
                return False


    server = GSIServer(('localhost', 3000), 'odM6BOq8stAsOpRJK4hb', RequestHandler)

    try:
        server.serve_forever()
    except:
        server.server_close()
        return snapshot
