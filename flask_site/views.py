from flask import request, redirect, url_for, render_template, flash, session, jsonify
from flask_site import app, socketio
from sqlalchemy import create_engine
import json
from flask_socketio import send, emit
import subprocess

@app.route('/')
def show_entries():
    dns_dict = {}

    engine = create_engine('mysql://root:pass@localhost/infra?charset=utf8mb4')
    with engine.connect() as con:
        rows = con.execute("select * from dns")
    for i in rows:
        dns_dict[i[0]] = {"ip": "{}".format(i[1]), "domain": "{}".format(i[2]), "username": "{}".format(i[4])}

#    print(dns_dict)
#    for i in range(1,255):
#        dns_dict[i] = {"ip": "192.168.100.{}".format(i)}
    return render_template('entries/index.html', dns_dict=dns_dict)

@app.route('/', methods=['post'])
def get_list():
    a = request.json['a']
    b = request.json['b']
    c = request.json['c']
    print(a)
    print(b)
    print(c)
    engine = create_engine('mysql://root:pass@localhost/infra?charset=utf8mb4')
    with engine.connect() as con:
        rows = con.execute("select * from dns")
    for i in rows:
        print(i)
    return_data = {"a":'{}'.format(a), "b":'{}'.format(b), "c":'{}'.format(c)}
    return jsonify(ResultSet=json.dumps(return_data))

@app.route('/apply', methods=['post'])
def update_list():
    boke = subprocess.run("date +%S_%3N", shell= True, stdout=subprocess.PIPE)
    boke = boke.stdout.strip().decode('utf8')

    make_lock(boke)
    lock_flag = check_lock()

    if 2 < lock_flag:
#    if 1 > 0:
        delete_lock(boke)
        return 'hage'
    else:
        id = request.json['id']
        ip = request.json['ip']
        domain = request.json['domain']
        username = request.json['username']
    
        print('--- --- --- --- --- ')
        print(id)
        print(ip)
        print(domain)
        print(username)
        print('--- --- --- --- --- ')
    
    
        engine = create_engine('mysql://root:pass@localhost/infra?charset=utf8mb4')
        with engine.connect() as con:
            try:
                rows = con.execute("update dns set ip = '{}', domain = '{}', username = '{}' where id = '{}' ".format(ip, domain, username, id))
            except:
                print('--- --- --- --- --- ')
                print('update done !!!!!!!!!!!!!!!')
                print('--- --- --- --- --- ')
                import traceback
                traceback.print_exc()
        print('update done !!!!!!!!!!!!!!!')
        update_dns()
        delete_lock(boke)
        modal_form(id, ip, domain, username)
        not_modal_form(id, domain, username)
    
    
        engine = create_engine('mysql://root:pass@localhost/infra?charset=utf8mb4')
        with engine.connect() as con:
            rows = con.execute("select ip, domain, username from dns where id = '{}'".format(ip, domain, username, id))
        for i in rows:
            ip = i[0]
            domain = i[1]
            username = i[2]
    
    #    return jsonify(ResultSet=json.dumps({"a" :id, "b": 'yabai'}))
        return jsonify(ResultSet=json.dumps({"id": id, "ip": ip, "domain": domain, "username": username}))

def make_lock(arg):
    res = subprocess.run('ssh 192.168.100.53 "touch lock/{}"'.format(arg), shell=True)
    

def check_lock():
    res = subprocess.run('ssh 192.168.100.53 "ls lock| wc -l"', shell=True, stdout=subprocess.PIPE)
    print(res)
    return(int(res.stdout.strip().decode('utf8')))

def delete_lock(arg):
    res = subprocess.run('ssh 192.168.100.53 "rm lock/{}"'.format(arg), shell=True, stdout=subprocess.PIPE)
    

def update_dns():
    subprocess.run('ssh 192.168.100.53 "touch hage"', shell=True)
    print('updateeeeeeeeeeeeeeeeeeeeeee')
    

@app.route('/clear', methods=['post'])
def clear_form():
    ip = ""
    id = request.json['id']
    engine = create_engine('mysql://root:pass@localhost/infra?charset=utf8mb4')
    with engine.connect() as con:
        rows = con.execute("update dns set domain = '', username = '' where id = {}".format(id))
        rows2 = con.execute("select ip from dns where id = {}".format(id))
    for i in rows2:
        ip = i[0]
    modal_form(id, ip, '', '')
    not_modal_form(id, '', '')
    return 'delete success'


@app.route('/chat', methods=['post'])
def hage():
    socketio.emit('some event', {'data': 42})
    return 'chat test'

def modal_form(id, ip, domain, username):
    socketio.emit('modal_form', {'id': id, 'ip': id, 'domain': domain, 'username': username})
    return 'modal_form success!'

def not_modal_form(id, domain, username):
    socketio.emit('not_modal_form', {'id': id, 'domain': domain, 'username': username})
    return 'not_modal_form success!'

