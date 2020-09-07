import sqlite3
from passlib.apps import custom_app_context as pas_hasher
import pickle
from time import time
import hashlib

conn = sqlite3.connect('chatdb.db')
c = conn.cursor()

c.execute('PRAGMA foreign_keys = ON')
c.execute(f"""CREATE TABLE IF NOT EXISTS users(
            userid integer NOT NULL PRIMARY KEY ,
            username text NOT NULL UNIQUE,
            password text NOT NULL
            )""")

# c.execute(f"""CREATE TABLE IF NOT EXISTS clients(
#             username text NOT NULL REFERENCES users(username),
#             friend text NOT NULL REFERENCES users(username),
#             hashcode text NOT NULL,
#             user_ip blob,
#             friend_ip blob
#             )""")

def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls

@auto_str
class Client():
    def __init__(self, username,friendname,hashcode, user_ip, friend_ip=None):
        self.username = username
        self.friendname = friendname
        self.hashcode = hashcode
        self.user_ip = user_ip
        self.friend_ip = friend_ip

    def __repr__(self):
        return str(self)

def find(arr, att_name, att):
    condition = ''
    for i, x, y in zip(range(len(att_name)),att_name, att):
        if not condition:
            condition = condition  + f'x.{x} == att[{i}]'
        else:
            condition = condition  + ' and ' f'x.{x} == att[{i}]'
    for i, x in enumerate(arr):
        if eval(condition):
            return x




clients = []


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
    c.execute('SELECT * FROM users where username=? LIMIT 1', (username,))
    user = c.fetchall()
    if user:
        hashpas = user[0][2]
        if pas_hasher.verify(password, hashpas):
            print('login in sucessfull')
            return True
        else:
            print('invalid password')
            return False
    else:
        print('user not found')
        return False


def start_chat(username, password, friend_name, user_ip):
    # user_ip = pickle.dumps(user_ip)
    if login(username, password):
        temp = pickle.dumps((username, password, friend_name, time()))
        hashcode = hashlib.sha3_512(temp).hexdigest()
        c.execute("SELECT * FROM users Where username==?",(friend_name,))
        temp = c.fetchall()

        if temp:
            # c.execute('SELECT user_ip from clients where username=? AND friend=? AND friend_ip=?',
            #           (friend_name, username, ''))

            friend=find(clients,['username','friendname','friend_ip'],[friend_name,username,None])
            # friend = c.fetchall()
            if friend:
                friend_ip = friend.user_ip
                clients.append(Client(username, friend_name, hashcode, user_ip, friend_ip))
                # c.execute('INSERT INTO clients VALUES(?,?,?,?,?)',
                #           (username, friend_name, hashcode, user_ip, friend_ip ))


                temp = find(clients,['username','friendname','friend_ip'],[friend_name, username, None])
                temp.friend_ip = user_ip
                temp=''
                # c.execute('UPDATE clients SET friend_ip=? WHERE username=? AND friend=? AND friend_ip=?',
                #           (user_ip, friend_name, username, None))
            else:
                # c.execute('INSERT INTO clients VALUES(?,?,?,?,?)',
                #           (username, friend_name, hashcode, user_ip, ''))
                clients.append(Client(username, friend_name, hashcode, user_ip, None))
            return hashcode
        else:
            return False
    else:
        print('invalid password')
        return False


def get_friend_ip(hashcode):
    # c.execute("SELECT friend_ip FROM clients WHERE hashcode==? LIMIT 1", (hashcode,))
    # friend_ip = c.fetchall()
    # if friend_ip:
    #     return pickle.loads(friend_ip[0][0])
    # else:
    #     return ''
    user = find(clients,['hashcode'],[hashcode])
    if user:
        return user.friend_ip
    else:
        return ''


def logout(username, friendname, hashcode):
    # c.execute('DELETE FROM clients WHERE hashcode==?', (hashcode,))
    temp = find(clients,['hashcode'],[hashcode])
    clients.remove(temp)
    temp=''

    # c.execute('UPDATE clients set friend_ip = ? WHERE username==? AND friend ==? ', ('', friendname, username))
    temp = find(clients,['username','friendname'],[username,friendname])
    temp.friend_ip=None


def logout_ip(user_ip):
    # c.execute('DELETE FROM clients WHERE user_ip==?', (user_ip,))
    temp = find(clients,['user_ip'],[user_ip])
    clients.remove(temp)
    temp=''
    # c.execute('UPDATE clients set friend_ip = ? WHERE friend_ip==? ', ('', user_ip))
    temp = find(clients,['friend_ip'],[user_ip])
    clients.remove(temp)