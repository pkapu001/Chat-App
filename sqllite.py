import sqlite3

conn = sqlite3.connect('chatdb.db')
c = conn.cursor()

c.execute('PRAGMA foreign_keys = ON')
c.execute(f"""CREATE TABLE IF NOT EXISTS users(
            userid integer NOT NULL PRIMARY KEY ,
            username text NOT NULL UNIQUE,
            password text NOT NULL
            )""")

c.execute(f"""CREATE TABLE IF NOT EXISTS clients(
            username text NOT NULL REFERENCES users(username),
            friend text NOT NULL REFERENCES users(username),
            hashcode text NOT NULL,
            user_ip blob,
            friend_ip blob            
            )""")


a = {'id': None, 'username': 'raj', }
b = {'id': None, 'username': 'tony', }
d = {'id': None, 'username': 'rupam', }
# e={'id':None,'username':None,}

l = [a, b, d]
try:
    c.executemany("INSERT INTO users VALUES (:id,:username)", l)
except sqlite3.IntegrityError as e:
    if 'UNIQUE constraint failed' in e.__str__():
        pass

c.execute("INSERT INTO users VALUES (:username, :friend  )", b)
c.executemany("INSERT INTO users VALUES (:username, :friend ,:number )", l)

c.execute('SELECT userid FROM users where username=?', ('tony',))

c.execute('SELECT * FROM users WHERE username=:user AND friend= :friend ', {'user': 'raj', 'friend': 'prem'})
c.execute('UPDATE users SET user=:n  WHERE username== :user AND friend=:friend  ', {'n': None, 'user': 'tony', 'friend': 'prem'})
c.execute('DELETE FROM clients')
c.execute('VACUUM')
c.execute('SELECT * FROM users')


x =c.fetchall()
c.execute("INSERT INTO clients VALUES(:userid,:username,:friend  )",
          {'userid':1,'username':'ror','friend':'prem'})

c.execute('SELECT * FROM clients')
c.fetchall()
conn.commit()

'''
=========================================================
'''




from passlib.apps import custom_app_context as pas_hasher
import pickle
from time import time
import hashlib
def signup(username, password):
    password = pas_hasher.hash(password)
    try:
        c.execute('INSERT INTO users VALUES(?,?,?)', (None, username, password))
        return True
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in e.__str__():
            print('username not available')
            return False

def login(username, password):
    c.execute('SELECT * FROM users where username=? LIMIT 1',(username,))
    user = c.fetchall()
    if user:
        hashpas = user[0][2]
        if pas_hasher.verify(password,hashpas):
            print('login in sucessfull')
            return True
        else:
            print('invalid password')
            return False
    else:
        print('user not found')
        return False


def start_chat(username, password, friend_name,user_ip):

            if login(username,password):
                temp = pickle.dumps((username, password, friend_name, time()))
                hashcode = hashlib.sha3_512(temp).hexdigest()
                try:
                    c.execute('SELECT user_ip from clients where username=? AND friend=? AND friend_ip=?', (friend_name, username, ''))
                    friend_ip = c.fetchall()
                    if friend_ip:
                        c.execute('INSERT INTO clients VALUES(?,?,?,?,?)', (username, friend_name, hashcode, user_ip, friend_ip[0][0]))
                        c.execute('UPDATE clients SET friend_ip=? WHERE username=? AND friend=? AND friend_ip=?',(user_ip,friend_name,username,''))
                    else:
                        c.execute('INSERT INTO clients VALUES(?,?,?,?,?)',(username,friend_name,hashcode,user_ip,''))
                    return hashcode
                except sqlite3.IntegrityError as e:
                    return False
            else:
                print('invalid password')
                return False


def get_friend_ip(hashcode):
    c.execute("SELECT friend_ip FROM clients WHERE hashcode==? LIMIT 1",(hashcode,))
    friend_ip=c.fetchall()
    if friend_ip:
        return friend_ip[0][0]
    else:
        return ''

def logout(username, friendname,hashcode):
    c.execute('DELETE FROM clients WHERE hashcode==?',(hashcode,))
    c.execute('UPDATE clients set friend_ip = ? WHERE username==? AND friend ==? ',('',friendname,username))


def logout_ip(username, friendname,user_ip):
    c.execute('DELETE FROM clients WHERE user_ip==?',(user_ip,))
    c.execute('UPDATE clients set friend_ip = ? WHERE username==? AND friend ==? ',('',friendname,username))



users=[('darkdragon','welcome1'),('tony','welcome1'),('rupam','welcome1'),('prem','welcome1')]
chat=[('darkdragon','welcome1','prem',1),('tony','welcome1','www',2),('rupam','welcome1','darkdragon',3),('prem','welcome1','darkdragon',4)]
users_false=[('darkdrag','welcome1'),('tony','welcom'),('rup','welcom'),('prem','welcome1')]

for u,p in users_false:
    login(u, p)

u,p,f,ip =chat[3]
start_chat(u,p,f,ip)

for u, p, f, ip in chat:
    print(start_chat(u, p, f, ip))

log_out = [('prem', 'darkdragon', '1fd70f99ac200e20724e4a2c560343d82e88d562c040c10eba7bb04a78b432d80c858c43709fda6d471'
                                  'c83ef3823896e3173b88a1bfb295ac3fc8339e2637feb'),
           ('rupam', 'darkdragon', '400730bdeca21d734272e5807461f48887843a98721ce6cc03d1e2a55a89d17ea7f46a6cfbbedc912e'
                                   '65505208c044b47b61886e0af68dfd9011e127705bae31')
           ]

for u,f,h in log_out:
    logout(u,f,h)

conn.commit()