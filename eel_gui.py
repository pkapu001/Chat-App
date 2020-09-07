import eel
from threading import Thread
print('starting now')
eel.init('web')
@eel.expose
def getdata(u , f):
    global friend,username
    friend=f
    username= u
    # print(f'{username}, {friend}')
    eel.say_hello_js(username)

@eel.expose
def setdata():
    # print(f'inside setdata :{username}')
    return username,friend

@eel.expose
def sendmsg(m):
    print(f'other >> {m}')
    pass

def other_thread():

    while True:
        m = input(f'enter msg >>> ')
        if m :
            eel.receivemsg(m)


eel.start('index.html',size=[550,750], block=False)
# eel.say_hello_js('raaajjj!!!!')

t = Thread(target= other_thread)
t.start()

while True:
    eel.sleep(2)





