import random
import time
import json
from paho.mqtt import client as mqtt_client
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "pqThF7iliQEhsuaX18sK5ZEC7TR98VZYKXlnV4HJwpFykx5WsukdnfS3yXDkcXVuac5DCAm2SS8w7Mjck_Ccog=="
org = "cdv"
url = "http://localhost:8086"
bucket="tempproject"
broker = 's3463711.ala.eu-central-1.emqxsl.com'
port = 8883
topic = "cdv/temp/sensor"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'espchinatest'
password = "12345678%"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)


    client = mqtt_client.Client(client_id)
    # client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.tls_set(ca_certs='./data/emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client




def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = msg.payload.decode().replace("'", '"')
        dataset = json.loads(data)
        print(dataset)
        temperature = dataset['temperature']
        humidity = dataset['humidity']

        client = InfluxDBClient(url=url, token=token, org=org)

        point = Point("temperature") \
            .tag("location", "cdv") \
            .field("value", temperature)


        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, record=point)

        client.close()

        print("Dane zostały zapisane do InfluxDB")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()