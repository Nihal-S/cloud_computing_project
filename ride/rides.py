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
    conn = sqlite3.connect('Rides.db')
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
    conn = sqlite3.connect('Rides.db')
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


@app.route('/api/v1/rides', methods=['POST'])
def create_ride():
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        created_by = request.json['created_by']
        timestamp = request.json['timestamp']
        source = request.json['source']
        destination = request.json['destination']
        name = created_by
        names = requests.get('http://cc-a3-1486621832.us-east-1.elb.amazonaws.com/api/v1/users')
        names = names.json()
        #names = names.json()
        areanames = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "Areaname","columns":"Area_no","where":"Area_name!='hdughuhuhfguihufdhuidhgfuhduhgiu'"})
        areanames =areanames.json()
        #print(areanames)
        #l = []
        #for i in names:
        #    l.append(i[0])
        #names = l
        l = []
        #print(names)
        for i in areanames:
            l.append(str(i[0]))
        areanames = l
        if(not created_by or not timestamp or not source or not destination):
            return jsonify(), 204
        # print(name)
        # print(names)
        print(source)
        print(areanames)
        #print(areanames)
        # print(source,destination)
        # print(name in names)
        # print(validate(timestamp))
        # print(source in areanames)
        # print(destination in areanames)
        if(name in names and validate(timestamp) and str(source) in areanames and destination in areanames):
            print("inside ")
            insert = "'"+created_by+"',"+"'"+timestamp+"',"+"'"+source+"','"+destination+"'"
            print(insert)
            r = requests.post('http://0.0.0.0:80/api/v1/db/write', json={"insert": insert,"column":"created_by,timestamp,source,destination","table":"ride","what":"insert"})
            res = jsonify()
            # res.statuscode = 201
            return res, 201
        else:
            res = jsonify()
            # res.statuscode = 400
            return res, 400

@app.route('/api/v1/rides', methods=['GET'])
def upcoming_ride():
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        if request.method == "GET":
            source = request.args.get('source')
            destination = request.args.get('destination')
            areanames = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "Areaname","columns":"Area_no","where":"Area_name!='hdughuhuhfguihufdhuidhgfuhduhgiu'"})
            areanames = areanames.json()
            l = []
            for i in areanames:
                l.append(str(i[0]))
            areanames = l
            print(areanames)
            print(source in areanames)
            print(destination in areanames)
            if(not source or not destination):
                return jsonify(), 204
            if(source in areanames and destination in areanames):
                names = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "ride","columns":"ride_id,created_by,timestamp","where":"source='"+source+"' and destination='"+destination+"'"})
                names = names.json()
                l = []
                for i in names:
                    dict = {
                        "rideId":i[0],
                        "username":i[1],
                        "timestamp":i[2]
                    }
                    l.append(dict)

                return jsonify(l), 200
            else:
                res = jsonify()
                # res.statuscode = 400
                return res, 400
    except Exception as e:
        print(e)
        res = jsonify()
        # res.statuscode = 500
        return res, 500

@app.route('/api/v1/rides/<string:ride_id>', methods=['GET'])
def list_rides(ride_id):
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        ride_id = str(ride_id)  
        ride_ids = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "ride","columns":"ride_id","where":"source!='hasdfuhuhasujdhjkh'"})
        ride_ids = ride_ids.json()

        l = []
        for i in ride_ids:
            l.append(str(i[0]))
        ride_ids = l
        # print(ride_id)
        # print(ride_ids)
        if(not ride_id):
            return jsonify, 204
        if(ride_id in ride_ids):
            result = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "ride","columns":"ride_id,created_by,timestamp,source,destination","where":"ride_id='"+ride_id+"'"})
            result1 = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "join_ride","columns":"username","where":"ride_id='"+ride_id+"'"})
            result1 = result1.json()
            result = result.json()
            l = []
            for i in result1:
                l.append(i[0])
            result1 = l
            dict = {
                "rideId":result[0][0],
                "Created_by":result[0][1],
                "users":result1,
                "Timestamp":result[0][2],
                "source":result[0][3],
                "destination":result[0][4]
            }
            return jsonify(dict), 200
        else:
            res = jsonify()
            # res.statuscode = 400
            return res, 400
    except Exception as e:
        print(e)
        res = jsonify()
        # res.statuscode = 500
        return res, 500

@app.route('/api/v1/rides/<string:ride_id>', methods=['POST'])
def join_rides(ride_id):
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        ride_id = str(ride_id)
        ride_ids = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "ride","columns":"ride_id","where":"ride_id!='2341356'"})
        ride_ids = ride_ids.json()
        print(ride_ids)
        names = requests.get('http://cc-a3-1486621832.us-east-1.elb.amazonaws.com/api/v1/users')
        names = names.json()
        l = []
        for i in ride_ids:
            l.append(str(i[0]))
        ride_ids = l
        #l = []
        #for i in names:
        #    l.append(i[0])
        #names = l
        username = request.json['username']
        username = str(username)
        if(not ride_id):
            return jsonify(), 204
        # print(username in names)
        print(ride_id)
        print(ride_ids)
        print(ride_id in ride_ids)
        if((username in names) and ((ride_id) in ride_ids)):
            insert = "'"+ride_id+"','"+username+"'"
            requests.post('http://0.0.0.0:80/api/v1/db/write', json={"insert": insert,"column":"ride_id,username","table":"join_ride","what":"insert"})
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


@app.route('/api/v1/rides/<string:ride_id>', methods=['DELETE'])
def delete_ride(ride_id):
    try:
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        ride_id = str(ride_id)
        ride_ids = requests.post('http://0.0.0.0:80/api/v1/db/read', json={"table": "ride","columns":"ride_id","where":"ride_id!='2341356'"})
        ride_ids = ride_ids.json()
        l = []
        for i in ride_ids:
            l.append(i[0])
        ride_ids = l
        print(ride_ids)
        print(ride_id)
        if(int(ride_id) in ride_ids):
            requests.post('http://0.0.0.0:80/api/v1/db/write', json={"insert": "ride_id='"+ride_id+"'","column":"username,password","table":"ride","what":"delete"})
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

@app.route('/api/v1/db/clear', methods=['POST'])
def clear_db():
    try:
        conn = sqlite3.connect('Rides.db')
        c = conn.cursor()
        query = "DELETE FROM ride"
        c.execute(query)
        query = "DELETE FROM join_ride"
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


@app.route('/api/v1/rides/count', methods=['GET'])
def ride_count():
        f = open("count.txt","r")
        count = f.readline()
        count = int(count)
        count += 1 
        f.close()

        f = open("count.txt","w")
        f.write(str(count))
        f.close()
        conn = sqlite3.connect('Rides.db')
        c = conn.cursor()
        query = "SELECT COUNT(*) FROM ride"
        c.execute(query)
        res = c.fetchall()
        conn.commit()
        conn.close()
        res = "["+ str(res[0][0]) +"]"
        print(res)
        return res, 200
    

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
	app.run(host="0.0.0.0",port=80)
