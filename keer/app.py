# import subprocess
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import os


# class MyHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()

#         # Construct the path to main.py using os.path
#         app_path = os.path.join(os.path.dirname(__file__), 'main.py')

#         # Launch main.py using subprocess.Popen()
#         subprocess.Popen(["python", app_path])


# def run_server():
#     address = ('', 8000) # listen on all interfaces on port 8000
#     httpd = HTTPServer(address, MyHTTPRequestHandler)
#     print('Listening on {}:{}'.format(*address))
#     httpd.serve_forever()


# if __name__ == '__main__':
#     run_server()



from flask import Flask, request,render_template
variable="dummy"
app = Flask(__name__)

import pygame
import random
import time 
import csv_bs

@app.route('/',methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
         return render_template("frontend.html")
    else:
        import main_logic
        return render_template("sample.html")

if(__name__ == "__main__"): 
    app.run(debug=True)  