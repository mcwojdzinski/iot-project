import cv2
import time
from ultralytics import YOLO
import matplotlib.pyplot as plt
import random
from paho.mqtt import client as mqtt_client


broker = 's3463711.ala.eu-central-1.emqxsl.com'
port = 8883
topic = "cdv/aimaster"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'espchinatest'
password = "12345678%"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.tls_set(ca_certs='./data/emqxsl-ca.crt')
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# Ładowanie modelu YOLO
model = YOLO('yolov8m.pt')

def run():
    # client = connect_mqtt()

    # Inicjalizacja kamery
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Nie można otworzyć kamery.")
        return

    print("Uruchamianie wykrywania obiektów... Naciśnij 'q', aby zakończyć.")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Nie można odczytać klatki z kamery.")
            break

        # Wykonaj predykcję
        results = model(frame)

        # Narysuj wykrycia na klatce
        annotated_frame = results[0].plot()

        # Wyświetl wideo w czasie rzeczywistym
        cv2.imshow("YOLOv8 - Real-Time Detection", annotated_frame)

        # Wyodrębnij wykryte obiekty
        detected_objects = []
        for result in results:  # Przetwarzaj wyniki
            for box in result.boxes:
                class_id = int(box.cls)  # ID klasy
                class_name = model.names[class_id]  # Nazwa klasy
                detected_objects.append(class_name)

        # Wypisz wykryte obiekty w terminalu
        print("Detected objects:", set(detected_objects))

        # Wyślij wyniki przez MQTT (opcjonalne)
        # for msg in detected_objects:
        #     result = client.publish(topic, msg)
        #     time.sleep(1)

        # Naciśnij 'q', aby zakończyć
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Zwolnij zasoby kamery i zamknij okna
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()
