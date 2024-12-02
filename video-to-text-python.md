#### Opis ogólny

Ten skrypt łączy się z kamerą w celu wykrywania obiektów w czasie rzeczywistym za pomocą modelu YOLOv8 (od ultralytics). Wyniki wykrywania są publikowane na serwerze MQTT w celu ich udostępnienia innym aplikacjom.

#### Zastosowane biblioteki:

- **OpenCV** (`cv2`): Do obsługi kamery i wizualizacji wideo.
- **Ultralytics YOLO (`ultralytics`)**: Do wykrywania obiektów.
- **Paho MQTT** (`paho.mqtt`): Do komunikacji za pomocą protokołu MQTT.
- **Matplotlib** (`matplotlib.pyplot`): Dodatkowo, jeśli wizualizacja byłaby potrzebna.
- **Random**: Do generowania unikalnych identyfikatorów klienta MQTT.
- **Time**: Do wprowadzenia opóźnienia w wysyłaniu wiadomości.

---

#### Szczegóły implementacyjne:

1.  **Konfiguracja MQTT**:

    - Serwer MQTT (`broker`) i port: Wykorzystano serwer **EMQX** z szyfrowaniem TLS.
    - Dane logowania: Zdefiniowane `username` i `password` do uwierzytelniania.
    - TLS: Certyfikat używany do szyfrowania został skonfigurowany z pliku lokalnego.

2.  **Ładowanie modelu YOLO**:

    - Skorzystano z modelu YOLOv8 w wersji medium (`yolov8m.pt`), który umożliwia szybkie i dokładne wykrywanie obiektów.
    - Model można zmieniać (np. `yolov8n.pt` dla wersji lightweight).

3.  **Funkcje główne**:

    - `connect_mqtt()`: Tworzy i zwraca klienta MQTT po połączeniu z brokerem. Obsługuje szyfrowanie TLS.
    - `run()`: Inicjalizuje kamerę, wykonuje wykrywanie w czasie rzeczywistym i publikuje wykryte obiekty na brokerze MQTT.

4.  **Wykrywanie obiektów**:

    - Wykryte obiekty są wizualizowane w czasie rzeczywistym na klatkach wideo.
    - Identyfikatory i nazwy klas obiektów są wyciągane z wyników YOLO i drukowane w terminalu.
    - Wyniki są publikowane na kanale MQTT (`cdv/aimaster`).

5.  **Obsługa kamery**:

    - Użyto domyślnej kamery (indeks `0`).
    - Kod sprawdza, czy kamera jest dostępna.
    - Naciśnięcie `q` zatrzymuje pętlę wykrywania.

6.  **Publikowanie wyników na MQTT**:

    - Wykryte obiekty są przesyłane jako wiadomości MQTT.
    - Aby zmniejszyć liczbę wiadomości, wysyłanie jest ograniczone czasowo (`time.sleep(1)`).

---

#### Instrukcja użytkowania:

1.  **Zainstaluj wymagane biblioteki**:

    `pip install opencv-python ultralytics matplotlib paho-mqtt`

2.  **Certyfikat dla TLS**:

    - Pobierz i umieść plik `emqxsl-ca.crt` w katalogu `./data/`.
    -

3.  **Uruchomienie**:

    - Upewnij się, że kamera jest podłączona.
    - Uruchom skrypt:
      `python script_name.py`

4.  **Interakcja z MQTT**:

    - Wyniki są publikowane na kanale `cdv/aimaster`.
