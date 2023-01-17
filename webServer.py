import http.server
import socketserver


anything = "some string default that will be changed by godot"

PORT = 8000

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(('0.0.0.0', PORT), handler) as httpd:
   #socketserver.TCPServer()
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()