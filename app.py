from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Hello from container {socket.gethostname()}\n".encode())

print("Server starting on port 8000...")
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()