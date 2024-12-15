import asyncio
import torch
import cv2
import os
import random
import time
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
from faster_whisper import WhisperModel
from ultralytics import YOLO
from paho.mqtt import client as mqtt_client
from unidecode import unidecode
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration
SAMPLE_RATE = 48000
CHANNELS = 1
chunk_duration = 5
FRAME_INTERVAL = 0.5

# MQTT Configuration
broker = 's3463711.ala.eu-central-1.emqxsl.com'
port = 8883
username = 'espchinatest'
password = "12345678%"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# MQTT Topics
TOPIC_TRANS = "cdv/aivoice"
TOPIC_AIMASTER = "cdv/aivideo"
TOPIC_TEMP = "cdv/temp/sensor"

# InfluxDB Configuration
INFLUX_TOKEN = "pqThF7iliQEhsuaX18sK5ZEC7TR98VZYKXlnV4HJwpFykx5WsukdnfS3yXDkcXVuac5DCAm2SS8w7Mjck_Ccog=="
INFLUX_ORG = "cdv"
INFLUX_URL = "http://localhost:8086"
INFLUX_BUCKET = "tempproject"

# Initialize models
if torch.cuda.is_available():
    device = "cuda"
    print("Using GPU.")
    try:
        whisper_model = WhisperModel("turbo", device=device, compute_type="float16")
    except ValueError:
        print("GPU doesn't support float16, falling back to float32")
        whisper_model = WhisperModel("turbo", device=device, compute_type="float32")
else:
    device = "cpu"
    print("CUDA unavailable, using CPU.")
    whisper_model = WhisperModel("turbo", device=device, compute_type="int8")

yolo_model = YOLO('yolov8m.pt')

async def process_video(mqtt_client):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Cannot open camera.")
        return

    previous_objects = set()

    try:
        while True:
            start_time = time.time()
            
            ret, frame = camera.read()
            if not ret:
                print("Failed to capture frame.")
                break
            
            frame = cv2.resize(frame, (640, 480))
            results = yolo_model(frame, conf=0.5, iou=0.45, max_det=20, verbose=False)
            
            annotated_frame = results[0].plot(
                line_width=1,
                labels=True,
                conf=True,
                boxes=True
            )
            
            cv2.imshow("YOLOv8 Detection", annotated_frame)
            
            current_objects = set()
            for result in results:
                for box in result.boxes:
                    if box.conf.item() > 0.5:
                        class_id = int(box.cls)
                        class_name = yolo_model.names[class_id]
                        current_objects.add(class_name)
            
            if current_objects != previous_objects:
                if current_objects:
                    objects_str = ", ".join(sorted(current_objects))
                    print("Detected objects changed:", objects_str)
                    mqtt_client.publish(TOPIC_AIMASTER, objects_str)
                else:
                    print("No objects detected")
                    mqtt_client.publish(TOPIC_AIMASTER, "no objects")
                
                previous_objects = current_objects
            
            elapsed_time = time.time() - start_time
            await asyncio.sleep(max(0, FRAME_INTERVAL - elapsed_time))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        camera.release()

async def record_and_transcribe(mqtt_client):
    try:
        while True:
            audio_data = sd.rec(int(chunk_duration * SAMPLE_RATE), 
                              samplerate=SAMPLE_RATE, 
                              channels=CHANNELS, 
                              dtype='float32')
            sd.wait()
            
            # Calculate RMS to detect silence
            rms = np.sqrt(np.mean(np.square(audio_data)))
            silence_threshold = 0.01
            
            if rms < silence_threshold:
                print("Silence detected, skipping transcription")
                continue
            
            filename = "temp.wav"
            scaled_audio = np.int16(audio_data * 32767)
            write(filename, SAMPLE_RATE, scaled_audio)
            
            segments, info = whisper_model.transcribe(
                filename,
                word_timestamps=True,
                vad_filter=True,
                # vad_parameters=dict(
                #     min_silence_duration_ms=500,
                #     speech_pad_ms=400
                # )
            )
            
            message = ""
            for segment in segments:
                if segment.avg_logprob > -1.0:
                    for word in segment.words:
                        message += word.word + " "
            
            if message.strip():
                print("Transcription: ", message)
                msg = unidecode(message)
                mqtt_client.publish(TOPIC_TRANS, msg)
            
            await asyncio.sleep(0.1)
            
    except Exception as e:
        print(f"Error in audio processing: {e}")

def on_message(client, userdata, msg):
    try:
        if msg.topic == TOPIC_TEMP:
            data = msg.payload.decode().replace("'", '"')
            dataset = json.loads(data)
            print(f"Received temperature data: {dataset}")
            
            temperature = dataset['temperature']
            humidity = dataset['humidity']

            influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
            point = Point("temperature") \
                .tag("location", "cdv") \
                .field("value", temperature)

            write_api = influx_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=INFLUX_BUCKET, record=point)
            influx_client.close()

            print("Data saved to InfluxDB")
            
    except Exception as e:
        print(f"Error processing message: {e}")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(TOPIC_TEMP)
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.tls_set(ca_certs='./data/emqxsl-ca.crt')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client

async def main():
    mqtt_client = connect_mqtt()
    mqtt_client.loop_start()
    
    try:
        # Run both tasks concurrently
        await asyncio.gather(
            # process_video(mqtt_client),
            record_and_transcribe(mqtt_client)
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        cv2.destroyAllWindows()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 
