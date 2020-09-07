import logging
import select
import socket
from database import *

logging.basicConfig(level=logging.DEBUG)
log = logging.debug
headderlen = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 1028))
s.listen(5)

sockets_list = [s]


# clients = []
# users={}
# required=[]
#
# def find(arr, att_name, att):
#     for i, x in enumerate(arr):
#         if eval(f'x[att_name]== att '):
#             return x


def send_msg(clt, msg):
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


log('server started ....')
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == s:
            client, adr = s.accept()
            sockets_list.append(client)

        else:
            req = receivemsg(notified_socket)
            if req is False:
                #
                # c.execute('DELETE FROM clients WHERE user_ip == ? ', (notified_socket,))
                # c.execute('UPDATE CLIENTS SET friend_ip==? WHERE friend_ip == ?', ('', notified_socket))
                logout_ip(notified_socket)
                sockets_list.remove(notified_socket)
                continue

            else:
                print(req)
                if req['request'] == 'SEND MSG':  # SENDING MSG
                    friend_ip = get_friend_ip(req['hashcode'])
                    print(f'friend ip : {friend_ip}')
                    if friend_ip:
                        send_msg(friend_ip, req['msg'])
                    else:
                        send_msg(notified_socket, 'friend not yet connected')

                elif req['request'] == 'LOGIN':  # LOGIN
                    response = login(req['username'], req['password'])
                    print(response)
                    send_msg(notified_socket, response)

                elif req['request'] == 'SIGNUP':  # SIGNUP
                    response = signup(req['username'], req['password'])
                    send_msg(notified_socket, response)

                elif req['request'] == 'START CHAT':
                    response = start_chat(req['username'], req['password'], req['friend'], notified_socket)
                    print(response)
                    send_msg(notified_socket, response)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        logout_ip(notified_socket)
