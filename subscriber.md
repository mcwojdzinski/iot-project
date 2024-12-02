# Python - subscriber.py

### Moduły Python

Poniższe biblioteki Python są wymagane:

- `paho-mqtt`
- `influxdb-client`
- `json`
- `random`
  Aby zainstalować wymagane pakiety, użyj polecenia:
  `pip install paho-mqtt influxdb-client`

## Konfiguracja

### Zmienne globalne

- **InfluxDB**

  - `token`: Token autoryzacyjny do połączenia z bazą danych.
  - `org`: Organizacja używana w InfluxDB.
  - `url`: Adres URL serwera InfluxDB.
  - `bucket`: Nazwa bucketu w InfluxDB, gdzie dane będą zapisywane.

- **MQTT**

  - `broker`: Adres serwera MQTT.
  - `port`: Port używany do połączenia z serwerem MQTT (port TLS: 8883).
  - `topic`: Temat MQTT, z którego dane będą odbierane.
  - `client_id`: Identyfikator klienta MQTT generowany losowo.
  - `username`: Nazwa użytkownika MQTT.
  - `password`: Hasło użytkownika MQTT.

---

## Funkcje

### `connect_mqtt() -> mqtt_client`

Funkcja nawiązuje połączenie z serwerem MQTT.

- **Opis:**

  - Ustawia dane uwierzytelniające (`username` i `password`).
  - Konfiguruje TLS z wykorzystaniem certyfikatu (`./data/emqxsl-ca.crt`).
  - Obsługuje połączenie za pomocą callbacku `on_connect`.

- **Zwraca:** Obiekt klienta MQTT.

#### Callback: `on_connect(client, userdata, flags, rc)`

- **Parametry:**
  - `rc`: Kod zwrotu połączenia.
- **Działanie:**
  - Wyświetla komunikat, jeśli połączenie zostało nawiązane pomyślnie.

---

### `subscribe(client: mqtt_client)`

Funkcja subskrybuje temat MQTT i obsługuje odebrane wiadomości.

- **Opis:**
  - Subskrybuje temat określony w zmiennej `topic`.
  - Ustawia callback `on_message`.

#### Callback: `on_message(client, userdata, msg)`

- **Parametry:**
  - `msg`: Otrzymana wiadomość MQTT.
- **Działanie:**

  - Odbiera wiadomości w formacie JSON.
  - Dekoduje dane i parsuje je jako obiekt JSON.
  - Wyodrębnia wartości temperatury i wilgotności.
  - Tworzy punkt danych i zapisuje go w InfluxDB.
  - Zamyka połączenie z InfluxDB.

- **Opis:**
  - Inicjuje połączenie MQTT przez `connect_mqtt`.
  - Rozpoczyna subskrypcję przez `subscribe`.
  - Uruchamia nieskończoną pętlę odbierania wiadomości `client.loop_forever()`.

## Wymagania dodatkowe

- Certyfikat TLS (`emqxsl-ca.crt`) musi znajdować się w katalogu `./data/`.
- InfluxDB musi być dostępne pod adresem skonfigurowanym w zmiennej `url`.
- Serwer MQTT powinien działać i akceptować połączenia na podanym brokerze i porcie.

## Schemat działania

1.  Klient MQTT łączy się z serwerem.
2.  Odbiera wiadomości JSON z tematu MQTT.
3.  Dane są parsowane, a następnie zapisywane w InfluxDB jako punkt danych.

## Uwagi

- Kod obsługuje jedynie podstawowe scenariusze błędów, np. brak połączenia z MQTT.
- Należy upewnić się, że dane JSON zawierają pola `temperature` i `humidity`.

## Przykład wiadomości MQTT

Przykładowa wiadomość JSON, którą aplikacja może przetworzyć:

`{
  "temperature": 22.5,
  "humidity": 45
}`
