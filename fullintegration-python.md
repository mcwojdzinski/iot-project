## 1. Cel programu

Ten program realizuje integrację trzech głównych funkcji:
Analizę wideo w czasie rzeczywistym z wykorzystaniem YOLOv8 w celu wykrywania obiektów.
Transkrypcję audio za pomocą modelu Whisper.
Przechowywanie danych z czujników (temperatury i wilgotności) w bazie danych InfluxDB.
Dodatkowo dane są publikowane i odbierane za pomocą protokołu MQTT.

## 2. Konfiguracja

#### Konfiguracja podstawowa
* SAMPLE_RATE: Częstotliwość próbkowania dla audio (48000 Hz).
* CHANNELS: Liczba kanałów audio (1 - mono).
* chunk_duration: Długość nagrania audio w sekundach (5 sekund).
* FRAME_INTERVAL: Interwał przetwarzania wideo w sekundach (0.5 sekundy).

#### Konfiguracja MQTT
* broker: Adres brokera MQTT ("s3463711.ala.eu-central-1.emqxsl.com").
* port: Port brokera MQTT (8883).
* username/password: Dane logowania do brokera MQTT.
* client_id: Losowo generowany identyfikator klienta MQTT.

#### Tematy MQTT
* TOPIC_TRANS: Temat do publikacji transkrypcji ("cdv/aivoice").
* TOPIC_AIMASTER: Temat do publikacji wykrytych obiektów z analizy wideo ("cdv/aivideo").
* TOPIC_TEMP: Temat do odbierania danych z czujnika temperatury ("cdv/temp/sensor").

#### Konfiguracja InfluxDB
* INFLUX_TOKEN: Token uwierzytelniający dostęp do InfluxDB.
* INFLUX_ORG: Organizacja w InfluxDB ("cdv").
* INFLUX_URL: URL bazy danych ("http://localhost:8086").
* INFLUX_BUCKET: Nazwa bucketa ("tempproject").

## 3. Moduły używane w programie

* asyncio: Do obsługi równoczesnych zadań.
* torch: Do obsługi modeli opartych na PyTorch.
* cv2: Do analizy obrazu i wyświetlania wideo.
* numpy: Operacje na danych numerycznych.
* scipy.io.wavfile: Zapis danych audio do pliku WAV.
* sounddevice: Nagrywanie dźwięku w czasie rzeczywistym.
* faster_whisper: Szybsza implementacja modelu Whisper do transkrypcji.
* ultralytics: YOLOv8 do wykrywania obiektów w wideo.
* paho.mqtt: Klient MQTT do obsługi komunikacji.
* unidecode: Usuwanie znaków diakrytycznych z tekstu.
* json: Obsługa danych JSON.
* influxdb_client: Klient InfluxDB do zapisywania danych.

## 4. Funkcje

### 4.1 process_video(mqtt_client)

Opis:
Analizuje obraz w czasie rzeczywistym z kamery, wykrywa obiekty przy użyciu YOLOv8 i publikuje wyniki do MQTT.

Działanie:
Otwiera kamerę za pomocą cv2.VideoCapture(0).
Wczytuje klatki wideo, skaluje do 640x480 pikseli.
Przetwarza każdą klatkę przy użyciu YOLOv8 i rysuje wykryte obiekty na obrazie.
Porównuje aktualnie wykryte obiekty z poprzednimi, a jeśli wykrycia się zmieniły, publikuje wyniki do MQTT.
Wyświetla przetworzone wideo w oknie OpenCV.
Obsługuje zakończenie pracy przez naciśnięcie q.

### 4.2 record_and_transcribe(mqtt_client)

Opis:
Nagrywa dźwięk, transkrybuje go za pomocą modelu Whisper i publikuje wynik do MQTT.
Działanie:
Nagrywa audio przez sounddevice przez chunk_duration sekund.
Oblicza RMS, aby wykryć ciszę (jeśli wartość RMS < 0.01, ignoruje audio).
Zapisuje dane audio do pliku WAV.
Przetwarza plik za pomocą modelu Whisper.
Buduje wiadomość z transkrypcji i publikuje do MQTT.

### 4.3 on_message(client, userdata, msg)

Opis:
Obsługuje wiadomości przychodzące z tematu MQTT TOPIC_TEMP i zapisuje dane w InfluxDB.
Działanie:
Dekoduje wiadomość i przekształca na format JSON.
Odczytuje dane temperatury i wilgotności.
Tworzy punkt danych dla InfluxDB i zapisuje go w buckecie tempproject.

### 4.4 connect_mqtt()

Opis:
Łączy się z brokerem MQTT i subskrybuje odpowiednie tematy.
Działanie:
Tworzy klienta MQTT.
Konfiguruje dane logowania i certyfikaty TLS.
Subskrybuje TOPIC_TEMP po pomyślnym połączeniu.

### 4.5 main()

Opis:
Uruchamia główne zadania programu: transkrypcję audio i analizę wideo.
Działanie:
Łączy się z brokerem MQTT.
Rozpoczyna obsługę pętli MQTT.
Uruchamia zadania: record_and_transcribe() i (opcjonalnie) process_video().
Obsługuje zamykanie programu i zwalnianie zasobów.

## 5. Obsługa błędów

Program obsługuje wyjątki podczas transkrypcji audio, zapisu do InfluxDB oraz połączenia z MQTT, wyświetlając odpowiednie komunikaty.
Sprawdza dostępność kamery przed uruchomieniem analizy wideo.

## 6. Wymagania

Python 3.7+
Zainstalowane biblioteki:

```py pip install asyncio torch opencv-python numpy scipy sounddevice faster-whisper ultralytics paho-mqtt unidecode influxdb-client ```

Certyfikaty TLS do połączenia z brokerem MQTT (pliki .crt).

Dostęp do kamery i mikrofonu.

## 7. Jak uruchomić?

Skonfiguruj poprawnie brokera MQTT i InfluxDB.

Uruchom program:

python main.py

Aby zakończyć działanie, naciśnij Ctrl+C lub q w oknie wideo.
