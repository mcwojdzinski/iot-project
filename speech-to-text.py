import torch
import os
import random
import time
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
from faster_whisper import WhisperModel
from paho.mqtt import client as mqtt_client
from unidecode import unidecode

# Parametry nagrywania audio
SAMPLE_RATE = 48000
CHANNELS = 1

# MQTT
broker = 's3463711.ala.eu-central-1.emqxsl.com'
port = 8883
topic = "cdv/trans"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'espchinatest'
password = "12345678%"

chunk_duration = 5  

# Inicjalizacja modelu Whisper
if torch.cuda.is_available():
    device = "cuda"
    print("USING GPU.")
else:
    device = "cpu"
    print("CUDA unavailable, using CPU.")

model = WhisperModel("turbo", device=device, compute_type="float16" if device == "cuda" else "int8")


# Funkcje związane z nagrywaniem i zapisywaniem audio
def list_audio_devices():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"{i}: {device['name']} (Channels: {device['max_input_channels']})")
    return devices

def select_audio_device():
    devices = list_audio_devices()
    device_id = int(input("Choose recording device ID: "))
    print(f"Chose device: {devices[device_id]['name']}")
    return device_id

def record_audio(duration: int):
    print("Recording...")
    device_id = 0  # Domyślnie pierwsze urządzenie
    if device_id is not None:
        sd.default.device = device_id

    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32')
    sd.wait()  
    return recording

def save_audio_to_file(audio_data: np.ndarray, filename: str):
    scaled_audio = np.int16(audio_data * 32767)
    write(filename, SAMPLE_RATE, scaled_audio)
    print(f"Audio saved to {filename}")


# Funkcja do połączenia z brokerem MQTT
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.tls_set(ca_certs='./data/emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# Funkcja uruchamiająca cały proces
def run():
    client = connect_mqtt()

    while True:
        # Nagrywanie dźwięku
        audio_data = record_audio(chunk_duration)

        # Zapis do pliku
        filename = "temp.wav"
        save_audio_to_file(audio_data, filename)

        # Transkrypcja audio za pomocą modelu Whisper
        segments, info = model.transcribe(filename, word_timestamps=True)

        # Tworzenie wiadomości z transkryptu
        message = ""
        for segment in segments:
            for word in segment.words:
                message += word.word + " "

        # Drukowanie transkryptu i publikowanie do MQTT
        print("Transcription: ", message)
        msg = unidecode(message)  # Usuwanie znaków diakrytycznych
        result = client.publish(topic, msg)

        time.sleep(1)  # Czekaj przez 1 sekundę przed kolejnym nagraniem


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Error: {e}")
