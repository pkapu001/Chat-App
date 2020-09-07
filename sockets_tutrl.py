import pickle
import socket
import time
headderlen = 10
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', 1028))
s.listen(5)
print('server created ')
while True:
    clt ,adr  = s.accept()

    file = open('20.html', 'rb')  # open file , r => read , b => byte format
    response = file.read()
    file.close()
    mimetype = 'text/html'
    header = 'HTTP/1.1 200 OK\n'
    header += 'Content-Type: ' + str(mimetype) + '\n\n'
    final_response = header.encode('utf-8')
    final_response += response

    print(f'''connected to {adr}
            {clt}
                            
                             ''')
    # msg = ['hay baby how are you',123456,'asshole']
    msg = f'time is {time.time()}'
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{headderlen}}','utf-8')+msg
    clt.send(msg)
s.close()