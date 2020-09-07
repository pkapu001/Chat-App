import socket
import sys
import errno
import eel
from threading import Thread
eel.init('web')
import pickle
import select
import time

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

headersize=20


start =False

username = ''
friend = ''
password = ''
hashcode = ''
req = {}

def send_req(msg):
    msg = pickle.dumps(msg)
    msg = f'{len(msg):<{headersize}}'.encode('utf-8') + msg
    s.send(msg)

def receivemsg():
    try:
        msg_header = s.recv(headersize).decode('utf-8')
        if not len(msg_header):
            return False
        msg = s.recv(int(msg_header))
        msg = pickle.loads(msg)
        # print(f'in rec msg :{msg}')
        return msg
    except Exception:
        return False
#
# @eel.expose
# def getdata(u , f):
#     global friend,username,start
#     friend=f
#     username= u
#     print(f'{username}, {friend}')
#     username_e = pickle.dumps(username)
#     friend_e = pickle.dumps(friend)
#     username_e = f'{len(username_e):<{headersize}}'.encode('utf-8') + username_e
#     friend_e =f'{len(friend_e):<{headersize}}'.encode('utf-8') + friend_e
#     try:
#         s.connect(('godschat.gq', 1028))
#         s.setblocking(False)
#         s.send(username_e)
#         s.send(friend_e)
#         start = True
#     except Exception as e:
#         if e.errno != 10035:
#             print(str(e))
#
#     eel.say_hello_js(username)

@eel.expose
def signup(u,p):
    global username, password
    username ,password = (u,p)
    req = {
        'request':'SIGNUP',
        'username': username,
        'password': password
    }
    # print(req)
    send_req(req)
    msg = receivemsg()
    if msg:
        return msg
    return False

@eel.expose
def login(u,p):
    # print('login')
    global username, password
    username, password = (u, p)
    req = {
        'request': 'LOGIN',
        'username': username,
        'password': password
    }
    send_req(req)
    print(f'send rex next line')
    msg = receivemsg()
    # print(f'login : {msg}')
    return msg



@eel.expose
def startchat(fn):
    global username, password, friend, hashcode, req, start
    friend = fn
    msg = {
        'request': 'START CHAT',
        'username': username,
        'password': password,
        'friend': friend,
    }
    send_req(msg)
    msg = receivemsg()
    print(f"msg  = {msg}")
    if msg:
        hashcode =msg
        # print(hashcode)
        req = {
            'request':'',
            'username': username,
            'friend': friend,
            'hashcode': hashcode,
            'msg': ''
            }
        print(req)
        password=''
        s.setblocking(False)
        start=True
        return True
    return False




@eel.expose
def setdata():
    print(f'inside setdata :{username}')
    return username,friend

@eel.expose
def sendmsg(m):
    global req
    req['request']='SEND MSG'
    req['msg']=m
    send_req(req)


s.connect(('godschat.gq', 1028))
# s.setblocking(False)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()
options = {
    'port':0
}
eel.start('index.html',size=[550,750], options=options,  block=False)

while True:
    try:
        while start:
            msg_header = s.recv(headersize)
            if not len(msg_header):
                print('connection closed by server')
                sys.exit()
            msg_length = int(msg_header.decode('utf-8'))
            msg = s.recv(msg_length)
            msg = pickle.loads(msg)
            print(f'>>>{msg}')
            eel.receivemsg(msg)

    except Exception as e:
        if e.errno !=10035:
            print(str(e))
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print(f'reading error {str(e)}')
            sys.exit()
        continue
    eel.sleep(0.1)