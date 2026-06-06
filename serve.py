import http.server, ssl, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Files that must never be served over the network (private key, certs, logs).
BLOCKED_SUFFIXES = ('.pem', '.log', '.key')


class Handler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Disable directory listings.
        self.send_error(403, 'Directory listing disabled')
        return None

    def send_head(self):
        if self.path.lower().split('?', 1)[0].endswith(BLOCKED_SUFFIXES):
            self.send_error(403, 'Forbidden')
            return None
        return super().send_head()


server = http.server.HTTPServer(('0.0.0.0', 8443), Handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
server.socket = ctx.wrap_socket(server.socket, server_side=True)
print('Serving at https://192.168.1.26:8443/')
print('Press Ctrl+C to stop.')
server.serve_forever()
