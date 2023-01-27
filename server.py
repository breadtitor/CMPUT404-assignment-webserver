#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos guoqiaoxi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import  os
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8").split("\r\n")
        print ("Got a request of: %s\n" % self.data)
        
        request_line = self.data[0]
        method, request_URI, HTTP_version = request_line.split(' ')
        print ("this is request_line: %s\n" % request_line)
        print ("this is request_URI: %s\n" % request_URI)
        splitURI = request_URI.split('/')[1:]
    
        if splitURI[-1] == '':
            splitURI[-1] = 'index.html'
        file_path = '/'.join(['.','www']+splitURI)
        if splitURI[-1] == '/':
            splitURI[-1] += 'index.html'
        file_path = '/'.join(['.','www']+splitURI)
       
        if 'GET' not in method:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return
        if  'HTTP/1.1' not in HTTP_version and 'HTTP/1.0' not in HTTP_version    :
            self.request.sendall(bytearray("HTTP/1.1 505 HTTP Version Not Supported\r\n",'utf-8'))
            return
        if '..' in splitURI:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            return
        
        
        safecheck = []
        for i in splitURI:
            if i == '':
                continue
            safecheck.append(i)
        if len(safecheck) != len(splitURI):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            return
       
        if request_URI[-1] != '/' and os.path.isdir(file_path):
            self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\r\nLocation: {request_URI}/\r\n\r\n",'utf-8'))
        if os.path.exists(file_path) and os.path.isfile(file_path):
          
            content_type_header = ''
            if '.html' in splitURI[-1]:
                content_type_header = 'Content-Type: text/html\r\n'
            elif '.css' in splitURI[-1]:
                content_type_header = 'Content-Type: text/css\r\n'
            elif '.js' in splitURI[-1]:
                content_type_header = 'Content-Type: text/javascript\r\n'
            elif '.png' in splitURI[-1]:
                content_type_header = 'Content-Type: image/png\r\n'
            elif '.gif' in splitURI[-1]:
                content_type_header = 'Content-Type: image/gif\r\n'
            elif '.jpg' in splitURI[-1]:
                content_type_header = 'Content-Type: image/jpeg\r\n'
            elif '.ico' in splitURI[-1]:
                content_type_header = 'Content-Type: image/x-icon\r\n'
            elif '.svg' in splitURI[-1]:
                content_type_header = 'Content-Type: image/svg+xml\r\n'
            elif '.woff' in splitURI[-1]:
                content_type_header = 'Content-Type: font/woff\r\n'
            elif '.woff2' in splitURI[-1]:
                content_type_header = 'Content-Type: font/woff2\r\n'
            elif '.ttf' in splitURI[-1]:
                content_type_header = 'Content-Type: font/ttf\r\n'
            elif '.eot' in splitURI[-1]:
                content_type_header = 'Content-Type: font/eot\r\n'
            with open(file_path,'r') as file:
                data = '\r\n\r\n'+file.read()
                print(f'success:{file_path}')
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+content_type_header+data,'utf-8'))
            return
        else:
            
            # print(f'failed:{file_path}')
            self.request.sendall(bytearray(f"HTTP/1.1 404 Not Found\r\n",'utf-8'))
            return
        print ("this is URI_split: %s\n" % splitURI)
       # self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
