import torch
import os,time
import random

from paho.mqtt import client as mqtt_client

from transformers import pipeline

whisper = pipeline("automatic-speech-recognition", "openai/whisper-large-v3", torch_dtype=torch.float16, device="cuda:0")


def sanitize(text):
    words = text.split(' ')
    print(words)
    chunks = []
    temp = []
    for word in words:
        if len(' '.join(temp).replace(' ','')) + len(word) < 16:
            temp.append(word)
        else:
            chunks.append(' '.join(temp))
            temp = [word]

    return chunks


broker = 's3463711.ala.eu-central-1.emqxsl.com'
port = 8883
topic = "cdv/trans"
# generate client ID with pub prefix randomly
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
    client.tls_set(ca_certs='./emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def run():
    client = connect_mqtt()

    while True:

        files = os.listdir()
        print(files)
        
        transcription = whisper(f"C:/Users/bkrzyzan/Desktop/trans/{files[0]}")
        print(transcription["text"])

        messages = sanitize( transcription["text"])
        print(messages)

        for msg in messages:
            result = client.publish(topic, msg)
            time.sleep(4)
        #result = client.publish(topic, "Jezeli siegnac pamiecia, to wydaje mi sie, ze w zyciu plakalem dwa razy. Pierwszy raz, gdy Magda, zona Arciego, przestala byc wolna i drugi, gdy jechalem na rowerze i jaja wkrecily mi sie w szpryche.")
        print(result)
        #client.loop_forever()