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
def send_response(self, status_code, content_type, content):
        self.request.sendall(bytearray(f"HTTP/1.1 {status_code}\r\n",'utf-8'))
import  os
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8").split("\r\n")
        print ("Got a request of: %s\n" % self.data)
        request = self.data[0]
        method, requestURI, HTTPversion = request.split(' ')
        print ("this is request_line: %s\n" % request)
        print ("this is request_URI: %s\n" % requestURI)
        splitURI = requestURI.split('/')[1:]
    #deal with the requestURI
        if splitURI[-1] == '':
            splitURI[-1] += 'index.html'
        if splitURI[-1] == '/':
            splitURI[-1] += 'index.html'
        file_path = "./www/"+splitURI[-1]

        if 'GET' not in method:
            send_response(self,405,'text/html','405 Method Not Allowed')
           
            return
        if  'HTTP/1.1' not in HTTPversion and 'HTTP/1.0' not in HTTPversion    :
            send_response(self,505,'text/html','505 HTTP Version Not Supported') 
            return
        if '..' in splitURI:
            send_response(self,404,'text/html','404 Not Found')
           
           
            return
        
        
        safecheck = []

        for i in splitURI:
            # check if there is any illegal character in the URI
            if i == '' or i == '.' or i == '..' or i == ' ' or i == '  ' or i == '   ':
                continue
            safecheck.append(i)
        if len(safecheck) != len(splitURI):
            send_response(self,404,'text/html','404 Not Found')
            return
       
        if requestURI[-1] != '/' and os.path.isdir(file_path):
            send_response(self,301,'text/html','301 Moved Permanently')
            
        if os.path.exists(file_path) and os.path.isfile(file_path):
          
            content_type_header = 'defaulholder'
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
            with open(file_path,'r') as file:
                data = '\r\n\r\n'+file.read()
                print(f'success:{file_path}')
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+content_type_header+data,'utf-8'))
            return
        else:
            
            print(f'failed:{file_path}')
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
