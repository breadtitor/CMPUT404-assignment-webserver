import socketserver
import os
import mimetypes

class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request: %s" % self.data.decode())

        # parse the incoming request to get the resource requested
        request_lines = self.data.decode().split("\r\n")
        request_line = request_lines[0].split(" ")
        method, path, version = request_line
        print(f'{method}, {path}, {version}')

        # check if the request method is GET
        if method != "GET":
            self.send_error(405, "Method Not Allowed")
            return

        # check if the requested resource exists in the www directory
        resource_path = "." + path
        if not os.path.exists(resource_path):
            self.send_error(404, "Not Found")
            return

        # check if the requested resource is a file and not a directory
        if os.path.isfile(resource_path):
            with open(resource_path, "rb") as file:
                content = file.read()
                content_type, _ = mimetypes.guess_type(resource_path)
                self.send_response(200, "OK", content, content_type)
        else:
            self.send_error(404, "Not Found")

    def send_response(self, status_code, status_message, content, content_type):
        response = f"HTTP/1.1 {status_code} {status_message}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "\r\n"
        response = bytearray(response, "utf-8") + content
        self.request.sendall(response)

    def send_error(self, status_code, status_message):
        self.send_response(status_code, status_message, b"", "text/plain")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    server.serve_forever()
