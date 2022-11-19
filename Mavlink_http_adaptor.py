from __future__ import print_function
from http.server import HTTPServer, BaseHTTPRequestHandler
from Thirdparty.pixhawk_hardware import *
import json

data = {'result': 'HTTP SERVER OK'}
host = ('localhost', 19999)

class My_Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        data = {'result': 'HTTP SERVER OK'}
        # 发给请求客户端的响应数据
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    def do_POST(self):
        self.send_response(200)
        datas = self.rfile.read(int(self.headers['content-length']))
        print('headers', self.headers)
        print("-->> post:", self.path, self.client_address)
        data_str=str(datas,'utf-8')
        date_json=json.loads(data_str)
        print(data_str)
        print('json')
        print(date_json['cmd'])
        if date_json['cmd']=='arm':
            user_app.pixhawk.arm()
            print('arm')
        if date_json['cmd']=='disarm':
            user_app.pixhawk.disarm()
            print('disarm')
        if date_json['cmd']=='take_off':
            print(int(date_json['alt_value']))
            user_app.pixhawk.arm_and_takeoff('GUIDED',int(date_json['alt_value']))
            print('take_off')
        if date_json['cmd']=='land':
            user_app.pixhawk.land()
            print('land')
        if date_json['cmd']=='front':
            user_app.pixhawk.send_ned_velocity(1,0,0,1)
            print('front')
        if date_json['cmd']=='back':
            user_app.pixhawk.send_ned_velocity(-1, 0, 0,1)
            print('back')
        if date_json['cmd']=='left':
            user_app.pixhawk.send_ned_velocity(0,1,0,1)
            print('left')
        if date_json['cmd']=='right':
            user_app.pixhawk.send_ned_velocity(0,-1,0,1)
            print('right')
        if date_json['cmd'] == 'high':
            user_app.pixhawk.send_ned_velocity(0, 0, -1, 1)
            print('high')
        if date_json['cmd'] == 'low':
            user_app.pixhawk.send_ned_velocity(0, 0, 1, 1)
            print('low')
        if date_json['cmd'] == 'left_cirl':
            print('left_cirl')
        if date_json['cmd']=='right_cirl':
            print('right_cirl')
        date_json={}
        # 发给请求客户端的响应数据
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # self.wfile.write(json.dumps(data).encode())
        self.wfile.write(json.dumps(data).encode())
class User_app:
    def __init__(self,com,wait_ready,baud):
        self.pixhawk=Pixhawk(com,wait_ready,baud)
if __name__ == '__main__':
    
    user_app=User_app('COM6',True,57600)
    server = HTTPServer(host, My_Server)
    print("server启动@ : %s:%s" % host)
    server.serve_forever()


