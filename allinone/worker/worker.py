import sqlite3
import requests
import json
import pika
import sys
print("hi")
from kazoo.client import KazooClient
zk = KazooClient(hosts='zookeeper:2181')
zk.start()
zk.ensure_path("/CC")
global v
v = sys.argv[1]

def slave_first():
    response = requests.post('http://orchestrator:80/api/v1/db/new_slave')
    queries = response.json()
    print(queries)
    queries_already = []
    for query in queries:
        if(query not in queries_already):
            conn = sqlite3.connect('Rideshare.db')
            c = conn.cursor()
            # query = "SELECT * FROM users"
            c.execute(query)
            conn.commit()
            conn.close()
            queries_already.append(query)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel1 = connection.channel()

def callback(ch, method, properties, body):
    if(v == "0"):
        print("callbacking")
        print(" [x] %r" % body)
        slave(body.decode("utf-8"))

def master(data):
    conn = sqlite3.connect('Rideshare.db')
    c = conn.cursor()
    query = data
    c.execute(query)
    conn.commit()
    conn.close()
    message = query
    channel1.basic_publish(exchange='syncQ', routing_key='', body=message, properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    	))
    return "success"

def callback_master(ch, method, properties, body):
    print(body)
    master(body.decode("utf-8"))

def slave(data):
    conn = sqlite3.connect('Rideshare.db')
    c = conn.cursor()
    print(data)
    query = data
    c.execute(query)
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return json.dumps(rows)


def decide(data):
    global v
    if(v == 1):
        response = master(data)
    else:
        response = slave(data)
    # print(response)
    return response



def on_request(ch, method, props, body):
    n = body
    n = n.decode("utf-8")
    print(n)
    response = decide(n)
    print(response)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# queries = requests.post('http://172.17.0.1:12345/api/v1/db/new_slave')
# queries = json.loads(queries)

# print(queries)

# for query in queries:
#     conn = sqlite3.connect('Rideshare.db')
#     c = conn.cursor()
#     # query = "SELECT * FROM users"
#     c.execute(query)
#     conn.commit()
#     conn.close()

channel.basic_qos(prefetch_count=1)
# channel1.basic_qos(prefetch_count=1)
def changeToMaster(data):
    global connection,channel,channel1
    # channel1.stop_consuming()
    # channel.stop_consuming()
    global v
    v = 1
    print(data)
    print(data.path)
    data,stat = zk.get(data.path)
    print(data)
    if(data.decode("utf-8")=="slave"):
        return
    # connection.close()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel1 = connection.channel()
    # channel.queue_declare(queue='writeQ', durable=True)
    channel.basic_consume(queue='writeQ', on_message_callback=callback_master, auto_ack=True)
    channel1.exchange_declare(exchange='syncQ', exchange_type='fanout')
    print(" [x] Awaiting RPC requests as master")
    channel.start_consuming()

print(sys.argv)
print(v)
if(v == "1"):
    zk.create(path="/CC/node",value=b'master',ephemeral=True, sequence=True)
    channel.queue_declare(queue='writeQ', durable=True)
    channel.basic_consume(queue='writeQ', on_message_callback=callback_master, auto_ack=True)
    channel1.exchange_declare(exchange='syncQ', exchange_type='fanout')
    print(" [x] Awaiting RPC requests as master")
    channel.start_consuming()
else:
    slave_first()
    path = zk.create(path="/CC/node",value=b'slave',ephemeral=True, sequence=True)
    channel.queue_declare(queue='readQ', durable=True)
    channel.basic_consume(queue='readQ', on_message_callback=on_request)
    channel1.exchange_declare(exchange='syncQ', exchange_type='fanout')
    result = channel1.queue_declare(queue='', durable=True)
    queue_name = result.method.queue
    channel1.queue_bind(exchange='syncQ', queue=queue_name)
    channel1.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    zk.get(path, watch=changeToMaster)
    try:
        channel1.start_consuming()
        channel.start_consuming()
    except pika.exceptions.StreamLostError as e:
        print(e)
    