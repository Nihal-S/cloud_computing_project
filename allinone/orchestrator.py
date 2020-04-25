from flask import Flask, render_template, request, jsonify
import json
import requests
import sqlite3
import string
import datetime
import pika
import uuid
app = Flask(__name__)



# class writing(object):
#     def __init__(self):
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host='rabbitmq'))

#         self.channel = self.connection.channel()

#         result = self.channel.queue_declare(queue='writeResponseQ', durable=True)
#         self.callback_queue = result.method.queue

#         self.channel.basic_consume(
#             queue=self.callback_queue,
#             on_message_callback=self.on_response,
#             auto_ack=True)

#     def on_response(self, ch, method, props, body):
#         if self.corr_id == props.correlation_id:
#             self.response = body
#             ch.basic_ack(delivery_tag = method.delivery_tag)

#     def call(self, q , n):
#         self.response = None
#         self.corr_id = str(uuid.uuid4())
#         self.channel.queue_declare(queue = 'writeQ', durable=True)
#         self.channel.basic_publish(
#             exchange='',
#             routing_key='writeQ',
#             properties=pika.BasicProperties(
#                 reply_to=self.callback_queue,
#                 correlation_id=self.corr_id,
#             ),
#             body=n)
#         while self.response is None:
#             self.connection.process_data_events()
#         return (self.response.decode("utf-8"))

class reading(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='ResponseQ', durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag = method.delivery_tag)

    def call(self, q , n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.queue_declare(queue = 'readQ', durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key='readQ',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n)

        while self.response is None:
            #print("recieved nothing")
            self.connection.process_data_events()
        return (self.response.decode("utf-8"))

@app.route('/api/v1/db/write', methods=['POST'])
def write_db():
    print("write")
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
    # write = writing()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='writeQ', durable=True)

    channel.basic_publish(exchange='', routing_key='writeQ', body= query)
    print("sent query", query)
    connection.close()  
    # response = write.call("writeQ",query)
    # print(response)
    res = jsonify()
    return res, 201

#9
@app.route('/api/v1/db/read', methods=['POST'])
def read():
    print("read")
    table = request.json['table']
    columns = request.json['columns']
    where = request.json['where']
    query = "SELECT "+columns+" FROM "+table+" WHERE "+where
    print(query)
    reader = reading()
    response = reader.call("readQ",query)
    print(response)
    # response = fibonacci_rpc.call("readQ",1)
    # response = json.loads(response)
    print(response)
    return response, 200

@app.route('/api/v1/db/clear', methods=['POST'])
def clear_db():
    # print("Clearing DB")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='writeQ', durable=True)
    queries = []
    queries.append("DELETE FROM users")
    queries.append("DELETE FROM ride")
    queries.append("DELETE FROM join_ride")
    for query in queries:
        channel.basic_publish(exchange='', routing_key='writeQ', body= query)
        print("sent query", query)
    connection.close()  
    # response = write.call("writeQ",query)
    # print(response)
    res = jsonify()
    return res, 200


if __name__ == '__main__':
	app.debug=True    
	app.run(host="0.0.0.0",port=12345)