import socket
import pickle
import select
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('70.160.230.181',1028))
# s.connect((socket.gethostname(),1028))
headderlen = 10
while True:
    i = 0
    ful_msg =b''
    newmsg=True
    try:
        while True:
            msg = s.recv(1024)
            # print(msg.decode('utf-8'))
            if newmsg:
                msglen = int(msg[:headderlen])
                print(f'new msg lenght: {msglen}')
                newmsg = False
            ful_msg+=msg
            print(i)
            i+=1
            if len(ful_msg)-headderlen == msglen:
                print('full msg received')
                ful_msg = pickle.loads(ful_msg[headderlen:])
                print(ful_msg)
                newmsg = True
                ful_msg=b''
    except Exception as e:
        print(e)