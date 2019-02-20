from flask import request, redirect, url_for, render_template, flash, session, jsonify
from flask_site import app
from sqlalchemy import create_engine
import json

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


    return jsonify(ResultSet=json.dumps({"a" :id, "b": 'yabai'}))
#    return jsonify(ResultSet=json.dumps({"id": id, "ip": ip, "domain": domain, "username": username}))






