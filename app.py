from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import redis

r = redis.Redis(host="redis", port=6379)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        count = r.incr("visits")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Hello from container {socket.gethostname()} - visited {count} times\n".encode())

print("Server starting on port 8000...")
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()