# -*- coding: utf-8 -*-

from bottle import route, run, request, response, template, static_file, post, redirect, HTTPError
import rsa, base64, time, hashlib
privkey =  rsa.PrivateKey.load_pkcs1( open('d/priv.key').read() )

ADDR='elp'
FORUMURL='http://gk11.ru/user/auth'

def _uflt(u):
    return ' '.join(u.split())

def kvi_sign(user,addr,uid,ts):
    k = '%s\n%s,%s\nts/%s\n' % (user,addr,uid,ts)
    signature = rsa.sign(k, privkey, 'SHA-1')
    s = k + base64.urlsafe_b64encode(signature)
    return base64.urlsafe_b64encode(s)

@route('/')
def index_page():
    return '<a href="/sign/login">login</a> or <a href="/sign/reg">regiser</a>'

@route('/sign/reg')
def reg_page():
    return template('reg.tpl')

@route('/sign/login')
def login_page():
    return template('login.tpl')

@post('/sign/reg')
def mk_kvitok():
    user = _uflt(request.forms.uname.encode('utf-8'))
    if not user:
        return u'имя не задано'
    pass1 = request.forms.upass1.encode('utf-8')
    if request.forms.upass1 != request.forms.upass2:
        return u'два разных пароля, вы уж определитесь',
    if not pass1:
        return u'нет пароля'
    pass1 = hashlib.sha1(pass1).hexdigest()
    udb =  open('d/points.txt').read().splitlines()
    uid = None
    for i,n in enumerate(udb):
        uif = n.split(':',3)
        if uif[1] == pass1 and uif[2] == user:
            uid = i+1
            ts = uif[0]
            break
        elif uif[2] == user and uif[1] != pass1:
            return u'Пользователь уже существует. А его пароль - нет'
    if uid is None:
        ts = int(time.time())
        open('d/points.txt', 'a').write('%s:%s:%s\n' % (ts,pass1,user))
        uid = open('d/points.txt').read().splitlines().index('%s:%s:%s' % (ts,pass1,user)) + 1
    kvitok = kvi_sign(user,ADDR,uid,ts)
    return template('regok.tpl',user=user,uid=uid,addr=ADDR,ts=ts,kvitok=kvitok,forumurl=FORUMURL)

@post('/sign/login')
def mk_kvitok():
    user = _uflt(request.forms.uname.encode('utf-8'))
    pass1 = request.forms.upass1.encode('utf-8')
    pass1 = hashlib.sha1(pass1).hexdigest()
    udb =  open('d/points.txt').read().splitlines()
    for i,n in enumerate(udb):
        ts,sp,su = n.split(':',3)
        if sp == pass1 and su == user:
            kvitok = kvi_sign(su,ADDR,i+1,ts)
            if request.forms.plain:
                response.content_type='text/plain; charset=UTF-8'
                return ':' + kvitok + ':'
            else:
                return template('regok.tpl',user=user,uid=i+1,addr=ADDR,ts=ts,kvitok=kvitok,forumurl=FORUMURL)
    redirect('/sign/login')

@route('/sign/get-<f:re:pub-key|blacklist>')
def get_key(f):
    response.content_type='text/plain; charset=UTF-8'
    return open('d/pub.key' if f == 'pub-key' else 'd/blacklist.txt').read()

@route('/s/<f:path>')
def send_file(f):
    return static_file(f, root='./s')


run(host='127.0.0.1',port=15558,debug=True)
