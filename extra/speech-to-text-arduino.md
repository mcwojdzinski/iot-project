### [Powrot do dokumentacji](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/README.md)

## Opis ogólny

Projekt oparty na ESP8266 i protokole MQTT, który umożliwia odbiór wiadomości z brokera MQTT oraz wyświetlanie ich na wyświetlaczu LCD podłączonym do mikrokontrolera. Wykorzystuje także synchronizację czasu przez NTP (Network Time Protocol) oraz bezpieczne połączenie SSL/TLS do brokera MQTT. Wiadomości odbierane przez ESP8266 są wyświetlane na ekranie LCD w postaci przewijającego się tekstu.

## Wymagane biblioteki

Aby uruchomić ten kod, wymagane są następujące biblioteki:

-   **ESP8266WiFi** – umożliwia łączność z siecią WiFi.
-   **PubSubClient** – umożliwia komunikację z brokerem MQTT.
-   **Wire** – obsługuje komunikację I2C z wyświetlaczem LCD.
-   **LiquidCrystal_I2C** – pozwala na obsługę wyświetlacza LCD za pomocą interfejsu I2C.
-   **time.h** – umożliwia synchronizację czasu z serwerem NTP.
-   **BearSSL** – do obsługi połączeń SSL/TLS z brokerem MQTT.

Można je zainstalować za pomocą Menedżera Bibliotek w Arduino IDE.

## Parametry

### Parametry WiFi:

-   **ssid** – nazwa sieci WiFi (zmień na swoją sieć).
-   **password** – hasło do sieci WiFi (zmień na swoje hasło).

### Parametry MQTT:

-   **mqtt_broker** – adres brokera MQTT (w tym przypadku EMQX publiczny broker).
-   **mqtt_port** – port brokera (domyślnie 8883 dla połączenia TLS).
-   **mqtt_topic** – temat, na który ESP8266 subskrybuje wiadomości.
-   **mqtt_username** – użytkownik do logowania na brokerze MQTT.
-   **mqtt_password** – hasło użytkownika do logowania na brokerze MQTT.

### Parametry NTP:

-   **ntp_server** – adres serwera NTP do synchronizacji czasu (domyślnie `pool.ntp.org`).
-   **gmt_offset_sec** – przesunięcie strefy czasowej w sekundach.
-   **daylight_offset_sec** – przesunięcie dla czasu letniego w sekundach (domyślnie 0).

### Parametry I2C:

-   **SDA_PIN** – pin SDA (dane) dla komunikacji I2C (domyślnie D6).
-   **SCL_PIN** – pin SCL (zegar) dla komunikacji I2C (domyślnie D7).

## Funkcje

### `setup()`

Funkcja inicjalizuje połączenie z WiFi, synchronizuje czas przez NTP, ustawia połączenie z brokerem MQTT, oraz konfiguruje i inicjalizuje wyświetlacz LCD.

#### Parametry:

Brak.

#### Działanie:

1.  Uruchamia połączenie z WiFi.
2.  Synchronizuje czas za pomocą NTP.
3.  Ustawia połączenie z brokerem MQTT i subskrybuje temat.
4.  Inicjalizuje komunikację I2C i wyświetlacz LCD.

### `connectToWiFi()`

Łączy ESP8266 z siecią WiFi, używając danych zapisanych w zmiennych `ssid` i `password`.

#### Parametry:

Brak.

#### Działanie:

1.  Próbuj połączyć ESP8266 z siecią WiFi.
2.  Czeka na połączenie i wypisuje status na serial monitorze.

### `syncTime()`

Synchronizuje czas systemowy z serwerem NTP.

#### Parametry:

Brak.

#### Działanie:

1.  Inicjalizuje synchronizację z serwerem NTP.
2.  Czeka, aż czas zostanie zsynchronizowany.
3.  Wypisuje aktualny czas na serial monitorze.

### `connectToMQTT()`

Łączy ESP8266 z brokerem MQTT przy użyciu połączenia TLS i uwierzytelniania za pomocą certyfikatu SSL.

#### Parametry:

Brak.

#### Działanie:

1.  Łączy się z brokerem MQTT przy użyciu połączenia TLS.
2.  Jeśli połączenie jest udane, subskrybuje zadany temat `mqtt_topic`.
3.  W przypadku niepowodzenia, ponawia próbę połączenia.

### `mqttCallback()`

Funkcja wywoływana, gdy wiadomość zostanie odebrana z subskrybowanego tematu MQTT.

#### Parametry:

-   **topic** – temat, na którym została wysłana wiadomość.
-   **payload** – treść wiadomości.
-   **length** – długość wiadomości w bajtach.

#### Działanie:

1.  Odczytuje wiadomość przesłaną na zadany temat.
2.  Przewija tekst wiadomości na wyświetlaczu LCD, wyświetlając po jednym fragmencie co 250 ms.

### `loop()`

Funkcja główna, która sprawdza, czy połączenie z brokerem MQTT jest aktywne i jeśli nie, ponownie łączy się z brokerem.

#### Parametry:

Brak.

#### Działanie:

1.  Sprawdza, czy połączenie z brokerem MQTT jest aktywne.
2.  Jeśli połączenie jest nieaktywne, ponownie łączy się z brokerem.
3.  Obsługuje wiadomości z brokera, wywołując funkcję `mqttCallback()`.

## Przebieg działania

1.  **Uruchomienie skryptu**: Po uruchomieniu ESP8266, urządzenie próbuje połączyć się z siecią WiFi. Gdy połączenie jest udane, synchronizuje czas z serwerem NTP.
2.  **Połączenie z MQTT**: ESP8266 łączy się z brokerem MQTT, używając certyfikatu SSL do nawiązania bezpiecznego połączenia.
3.  **Subskrypcja tematu**: Po pomyślnym połączeniu z brokerem, urządzenie subskrybuje temat `cdv/trans`, czekając na wiadomości.
4.  **Wyświetlanie wiadomości na LCD**: Gdy wiadomość jest otrzymywana, jej zawartość jest wyświetlana na ekranie LCD, przewijając tekst co 250 ms.

## Przykład uruchomienia

1.  Skopiuj kod do Arduino IDE.
2.  Wybierz odpowiednią płytkę ESP8266 i port.
3.  Załaduj program do mikrokontrolera.
4.  Upewnij się, że Twoje WiFi oraz broker MQTT są dostępne i poprawnie skonfigurowane.

Po uruchomieniu ESP8266, urządzenie powinno połączyć się z WiFi, zsynchornizować czas z serwerem NTP, połączyć się z brokerem MQTT i wyświetlić wiadomości na wyświetlaczu LCD.
