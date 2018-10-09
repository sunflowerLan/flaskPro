# -*- coding: utf-8 -*-
import os
import json
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,jsonify
from flask_util_js import FlaskUtilJs

app = Flask(__name__)
fujs = FlaskUtilJs(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path,'bodyBuild.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))

@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

def content_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = content_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_records():
    db = get_db()
    cur = db.execute("select records.action_id,actions.action_name as action_name,actions.body_part,records.train_weight, records.rm,date(records.train_day,'unixepoch') as train_day from records join actions on actions.id = records.action_id order by records.train_day desc")
    records = cur.fetchall()
    return render_template('index.html',records=records)

@app.route('/get_action')
def get_action_name():
    body_name = request.args.get('body_part')
    db = get_db()
    cur = db.execute("select id,action_name from actions where body_part = ?",[body_name])
    action_name = [dict(id = row[0], action_name = row[1]) for row in cur.fetchall()]
    return jsonify(action_name)

@app.route('/delete_record')
def delete_record():
    action_id = request.args.get('action_id')
    train_day = request.args.get('train_day')
    db= get_db()
    db.execute("delete from records where action_id=? and train_day=strftime('%s',?)",[action_id,train_day]);
    db.commit()
    flash('delete successfully')
    return redirect(url_for('show_records'))

@app.route('/add_record',methods=['POST'])
def add_record():
    db = get_db()
    #如果重量或rm为空，就赋默认值0
    weight = request.form['weight'].strip() if request.form['weight'].strip() !='' else 0
    rm = request.form['rm'].strip() if request.form['rm'].strip() !='' else 0

    db.execute("insert into records(body_part,action_id,train_weight,rm,train_day) values(?,?,?,?,strftime('%s',?));",[request.form['body_part'],request.form['train_action'],weight,rm,request.form['train_day']])
    db.commit()
    flash('create successfully')
    return redirect(url_for('show_records'))

@app.route('/action')
def action_index():
    db = get_db()
    cur = db.execute("select * from actions where body_part = '胸部'")
    actions = cur.fetchall()
    return render_template('action_index.html',actions=actions)

@app.route('/action/add')
def add_action():
    return render_template('action_add.html')

@app.route('/action/create',methods=['POST'])
def create_action():
    db=get_db()
    db.execute("insert into actions(action_name,body_part) values(?,?)",[request.form['action_name'],request.form['body_part']])
    db.commit()
    flash('create successfully')
    return redirect(url_for('action_index'))

@app.route('/action/delete/<action_name>')
def delete_action(action_name):
    # body_name = request.args.get('body_part')
    # print "action_name:",action_name
    db = get_db()
    db.execute("delete from actions where action_name = ?",[action_name])
    db.commit()
    flash('delete successfully')
    return redirect(url_for('action_index'))

if __name__=='__main__':
    app.run(debug=True)
