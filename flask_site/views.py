from flask import request, redirect, url_for, render_template, flash, session, jsonify
from flask_site import app
from sqlalchemy import create_engine
import json

@app.route('/')
def show_entries():
    return render_template('entries/index.html')

@app.route('/', methods=['post'])
def update_list():
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

