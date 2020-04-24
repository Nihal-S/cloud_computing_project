import sqlite3
import requests
import json
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()


def master(data):
    conn = sqlite3.connect('Rides.db')
    c = conn.cursor()
    query = data
    c.execute(query)
    conn.commit()
    conn.close()
    return "success"


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
    if(sys.argv[1] == 1):
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

channel.basic_qos(prefetch_count=1)
print(sys.argv)
print(sys.argv[1])
if(sys.argv[1] == "1"):
    channel.queue_declare(queue='writeQ', durable=True)
    channel.basic_consume(queue='writeQ', on_message_callback=on_request)
    print(" [x] Awaiting RPC requests as master")
else:
    channel.queue_declare(queue='readQ', durable=True)
    channel.basic_consume(queue='readQ', on_message_callback=on_request)
    print(" [x] Awaiting RPC requests as slave")
channel.start_consuming()
