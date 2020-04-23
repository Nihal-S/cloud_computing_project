import sqlite3
import requests
import json


def master(data):
    conn = sqlite3.connect('Rides.db')
    c = conn.cursor()
    dataObj = JSON.parse(data)
    data = dataObj.json['insert']
    column = dataObj.json['column']
    table = dataObj.json['table']
    what = dataObj.json['what']
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
    return res


def slave(data):
    conn = sqlite3.connect('Rideshare.db')
    c = conn.cursor()
    dataObj = JSON.parse(data)
    table = dataObj.json['table']
    columns = dataObj.json['columns']
    where = dataObj.json['where']
    query = "SELECT "+columns+" FROM "+table+" WHERE "+where
    c.execute(query)
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return json.dumps(rows)