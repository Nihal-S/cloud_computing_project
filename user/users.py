from flask import Flask, render_template, request, jsonify
import json
import requests
import sqlite3
import string
import datetime
app = Flask(__name__)

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y:%S-%M-%H')
        return True
    except ValueError:
        return False

def if_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
        
@app.route('/api/v1/db/write', methods=['POST'])
def write_db():
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()
    data = request.json['insert']
    column = request.json['column']
    table = request.json['table']
    what = request.json['what']
    if(what == "delete"):
        print("deleting")
        print(data)
        query = "DELETE FROM "+table+" where "+data
    else:
        print("inserting")
        query = "INSERT INTO "+table+" ("+column+") "+"VALUES ("+data+")"
    c.execute(query)
    conn.commit()
    conn.close()
    res = jsonify()
    return res, 201

#9
@app.route('/api/v1/db/read', methods=['POST'])
def read():
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()
    table = request.json['table']
    columns = request.json['columns']
    where = request.json['where']
    query = "SELECT "+columns+" FROM "+table+" WHERE "+where
    c.execute(query)
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return json.dumps(rows)

@app.route('/api/v1/users', methods=['PUT'])
def add():
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        name = request.json['username']
        password = request.json['password']
        insert = "'"+name+"','"+password+"'"
        names = requests.post('http://127.0.0.1:80/api/v1/db/read', json={"table": "users","columns":"username","where":"username!='hdughuhuhfguihufdhuidhgfuhduhgiu'"})
        names = names.json()
        l = []
        for i in names:
            l.append(i[0])
        names = l
        if(len(password) == 40 and if_hex(password) and name not in names):
            requests.post('http://127.0.0.1:80/api/v1/db/write', json={"insert": insert,"column":"username,password","table":"users","what":"insert"})
            res = jsonify()
            #res.statuscode = 201
            return res, 201
        else:
            res = jsonify()
            #res.statuscode = 400
            return res, 400
    except Exception as e:
        print(e)
        res = jsonify()
        # res.statuscode = 500
        return res, 500


@app.route('/api/v1/users/<string:name>', methods=['DELETE'])
def delete(name):
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        name = str(name)
        names = requests.post('http://127.0.0.1:80/api/v1/db/read', json={"table": "users","columns":"username","where":"username!='hdughuhuhfguihufdhuidhgfuhduhgiu'"})
        names = names.json()
        l = []
        for i in names:
            l.append(i[0])
        names = l
        print(name)
        print(names)
        if(name in names):
            print("username='"+name+"'")
            requests.post('http://127.0.0.1:80/api/v1/db/write', json={"insert": "username='"+name+"'","column":"","table":"users","what":"delete"})
            res = jsonify()
            # res.statuscode = 201
            return res, 200
        else:
            res = jsonify()
            # res.statuscode = 400
            return res, 400
    except Exception as e:
        print(e)
        res = jsonify()
        # res.statuscode = 500
        return res, 500


@app.route('/api/v1/users', methods=['GET'])
def list_all_users():
    # try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        users = requests.post('http://127.0.0.1:80/api/v1/db/read', json={"table":"users","columns":"username","where":"username!='wdjfuhwiufhwihfhwjhf'"})
        users = users.json()
        l = [i[0] for i in users]
        if(len(l) == 0):
            return jsonify({}), 204
        else:
            return jsonify(l), 200

    # except Exception as e:
    #     print(e)
    #     res = jsonify()
    #     return res,500

@app.route('/api/v1/db/clear', methods=['POST'])
def clear_db():
    try:
        conn = sqlite3.connect('Users.db')
        c = conn.cursor()
        query = "DELETE FROM users"
        c.execute(query)
        conn.commit()
        conn.close()
        res = jsonify()
        return res, 200
    except Exception as e:
        print(e)
        res = jsonify
        return res, 500


@app.route('/api/v1/_count', methods=['GET'])
def count_l():
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count) 
        f.close()
        res = []
        res.append(count)
        res = str(res)
        return res,200
    except Exception as e:
        print(e)
        res = jsonify
        return res,500

@app.route('/api/v1/_count', methods=['DELETE'])
def count_reset():
    try:
        f = open("count.txt","w")
        f.write("0")
        f.close()
        res = jsonify()
        return res,200
    except Exception as e:
        print(e)
        res = jsonify
        return res,500

@app.errorhandler(405)
def method_not_allowed(e):
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        return {},405

if __name__ == '__main__':
	app.debug=True    
	app.run( host="0.0.0.0",port=80)
