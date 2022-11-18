"""gsi_pinger is used by the MainApp to ping CSGO for data in the form of a
snapshot of the round being spectated, for use by the predictive model.
This is done through the use of its Gamestate Intergration functionality."""


def pingerfunc():

    """The primary loop that opens a server, pings CSGO for a single snapshot,
    closes the server and makes snapshot data available to MainApp."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
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

            # Checks payload auth token against the token specified below
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
