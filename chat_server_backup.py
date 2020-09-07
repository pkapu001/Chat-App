import pickle
import socket
import errno
import time
import select
import logging,sys
from database import *

logging.basicConfig(level=logging.DEBUG)
log = logging.debug
headderlen = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('', 1028))
s.listen()

sockets_list=[s]
# clients = []
# users={}
# required=[]

def find(arr, att_name, att):
    for i,x in enumerate(arr):
        if eval(f'x[att_name]== att '):
            return  x


def send_msg(clt,msg):
    msg = pickle.dumps(msg)
    msg = f'{len(msg):<{headderlen}}'.encode('utf-8') + msg
    clt.send(msg)

def receivemsg(client_socket):
    try:
        msg_header = client_socket.recv(headderlen).decode('utf-8')
        if not len(msg_header):
            return False
        req = client_socket.recv(int(msg_header))
        req = pickle.loads(req)
        return req
    except:
        return False
log('debugging stateeee ....')
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list,[], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == s:
            client, adr = s.accept()
            # user = receivemsg(client)
            # if user is False:
            #     continue
            # friend = receivemsg(client)
            # if friend is False:
            #     continue
            # sockets_list.append(client)
            # friend = friend
            # user = user
            #
            # if user in required:
            #     x = find(clients,'friend_name',user)
            #     clients.append({'username': user,'user_ip':client, 'friend_name': friend,'friend_ip':x['user_ip']})
            #     x['friend_ip']=client
            #     log(f'found {friend} in reduired')
            #     log(f'{x}')
            #     required.remove(user)
            # else:
            #
            #     required.append(friend)
            #     clients.append({'username': user, 'user_ip': client, 'friend_name': friend, 'friend_ip': None})
            #     print('frined not online')
            #     send_msg(client,'your friend is not yet connected')
            # print(f'{user} connected from address: {adr} ')
        else:
            req = receivemsg(notified_socket)
            if req is False:
                user = find(clients,'user_ip',notified_socket)
                print(f'{user["username"]} disconnected!!!')
                sockets_list.remove(notified_socket)
                f = find(clients,'friend_name',user['username'])
                f['friend_ip']=None
                send_msg(f['user_ip'],'your friend has disconnected!')
                clients.remove(user)
                continue
            else:
                if req['request']== 'SEND MSG':  # SENDING MSG
                    friend_ip = get_friend_ip(req['hashcode'])
                    if friend_ip:
                        send_msg(friend_ip,req['msg'])
                    else:
                        send_msg(notified_socket,'friend not yet connected')

                elif req['request']== 'LOGIN':  # LOGIN
                    response = login(req['username'], req['password'])
                    send_msg(notified_socket,response)

                elif req['request'] == 'SIGNUP':  # SIGNUP
                    response = signup(req['username'],req['password'])
                    send_msg(notified_socket,response)

                elif req['request'] == 'START CHAT':
                    response = start_chat(req['username'],req['password'],req['friend'],notified_socket)



            user = find(clients,'user_ip',notified_socket)
            print(f'message from {user["username"]} >> {req}')
            if(user['friend_ip']):
                send_msg(user['friend_ip'],msg)
                print(f'sending msg to {user["friend_name"]}')
            else:
                send_msg(notified_socket,'friend not yet connected')

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        user = find(clients,'user_ip',notified_socket)
        f = find(clients,'friend_ip',notified_socket)
        f['friend_ip']=None
        clients.remove(user)
        print(f"{user['username']} been removed")
