## 1. Cel projektu

Projekt realizuje system IoT do monitorowania temperatury i wilgotności za pomocą ESP8266, czujnika DS18B20 oraz komunikacji MQTT. Dodatkowo dane są wyświetlane na ekranie LCD i przesyłane do brokera MQTT z użyciem bezpiecznego połączenia TLS.

## 2. Konfiguracja

#### Sprzęt
* ESP8266: Moduł mikrokontrolera z obsługą WiFi.
* DS18B20: Cyfrowy czujnik temperatury.
* Wyświetlacz LCD: 16x2 z komunikacją I2C.

#### Oprogramowanie
* Arduino IDE z zainstalowanymi bibliotekami:
* ESP8266WiFi: Obsługa WiFi.
* PubSubClient: Obsługa MQTT.
* DallasTemperature: Obsługa czujnika DS18B20.
* LiquidCrystal_I2C: Obsługa wyświetlacza LCD.

#### Ustawienia WiFi
* ssid: Nazwa sieci WiFi.
* password: Hasło do sieci WiFi.
* Ustawienia MQTT
* mqtt_broker: Adres brokera MQTT.
* mqtt_port: Port brokera MQTT (TLS).
* mqtt_username/mqtt_password: Dane uwierzytelniające do MQTT.

#### Tematy MQTT:

* cdv/temp/sensor: Publikacja danych temperatury.
* cdv/aivideo i cdv/aivoice: Odbiór wiadomości dotyczących analizy wideo i głosu.

#### Ustawienia NTP

* ntp_server: Serwer synchronizacji czasu.
* gmt_offset_sec: Różnica czasowa w sekundach (dla strefy czasowej).
* daylight_offset_sec: Korekta na czas letni.

## 3. Funkcje

### 3.1 setup()

Opis:
Inicjalizuje komponenty: WiFi, MQTT, czujnik DS18B20, wyświetlacz LCD oraz synchronizację czasu.

Kroki:
Ustawienie komunikacji z wyświetlaczem LCD.
Połączenie z siecią WiFi.
Synchronizacja czasu z serwerem NTP.
Konfiguracja klienta MQTT i połączenie z brokerem.

### 3.2 connectToWiFi()

Opis:

Łączy się z siecią WiFi, czekając na ustanowienie połączenia.

### 3.3 syncTime()

Opis:

Synchronizuje czas z serwerem NTP, wymaganym dla poprawnej walidacji certyfikatów SSL.

### 3.4 connectToMQTT()

Opis:

Łączy się z brokerem MQTT z użyciem certyfikatu SSL.

Subskrybuje tematy cdv/aivideo i cdv/aivoice.

**3.5 mqttCallback(char topic, byte payload, unsigned int length)

Opis:

Obsługuje wiadomości przychodzące na subskrybowane tematy MQTT.

Aktualizuje wyświetlany tekst na LCD w zależności od tematu wiadomości.

### 3.6 loop()

Odczytuje dane z czujnika temperatury i publikuje je na temat cdv/temp/sensor.
Wyświetla wiadomości na LCD z funkcją przewijania długiego tekstu.
Utrzymuje połączenie z brokerem MQTT.
Działanie:
Żąda odczytu temperatury z czujnika DS18B20.
Publikuje dane w formacie JSON na temat cdv/temp/sensor.
Wyświetla wiadomości z tematów cdv/aivideo i cdv/aivoice z funkcją przewijania tekstu.

### 3.7 Wyświetlanie przewijającego się tekstu

Jeśli długość tekstu przekracza 16 znaków, włącza się mechanizm przewijania.
Po zakończeniu przewijania tekst jest resetowany do początku.

## 4. Format danych MQTT

Publikowane dane na temat cdv/temp/sensor:
``
{
  "temperature": 25.3,
  "humidity": 55
}
``

## 5. Obsługa błędów

Połączenie WiFi: Program próbuje ponownie połączyć się co sekundę, jeśli nie ma dostępu do sieci.
MQTT: W przypadku zerwania połączenia program automatycznie próbuje je wznowić.
Czujnik DS18B20: Jeśli czujnik jest odłączony, wyświetlany jest komunikat o błędzie w monitorze szeregowym.

## 6. Wymagania

* ESP8266 z zainstalowanym środowiskiem Arduino IDE.
* Biblioteki Arduino:
* ESP8266WiFi
* PubSubClient
* DallasTemperature
* LiquidCrystal_I2C
* Broker MQTT obsługujący TLS (np. EMQX).
* Dostęp do serwera NTP dla synchronizacji czasu.
* Certyfikat SSL brokera MQTT.

## 7. Jak uruchomić?

* Skonfiguruj dane WiFi i MQTT w kodzie.
* Wgraj kod na ESP8266 za pomocą Arduino IDE.
* Uruchom monitor szeregowy, aby monitorować status połączenia i dane.
* Obserwuj dane na wyświetlaczu LCD oraz publikacje w brokerze MQTT.
