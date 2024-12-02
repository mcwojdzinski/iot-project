### [Powrot do dokumentacji](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/README.md)

#### Opis ogólny:

Skrypt jest przeznaczony do pracy z mikrokontrolerem **ESP8266**. Wykorzystuje bibliotekę **PubSubClient** do komunikacji za pomocą protokołu MQTT oraz **WiFi** do łączenia się z siecią. Program obsługuje synchronizację czasu za pomocą **NTP**, a także wyświetlanie otrzymanych wiadomości MQTT na ekranie LCD z interfejsem **I2C**.

#### Zastosowane biblioteki:

- **ESP8266WiFi**: Do obsługi połączenia WiFi.
- **PubSubClient**: Do obsługi komunikacji MQTT.
- **Wire**: Do komunikacji I2C z wyświetlaczem LCD.
- **LiquidCrystal_I2C**: Do sterowania wyświetlaczem LCD za pomocą I2C.
- **time.h**: Do synchronizacji czasu z serwerem NTP.
- **BearSSL::WiFiClientSecure**: Do nawiązywania bezpiecznego połączenia (TLS) z brokerem MQTT.

#### Funkcjonalności:

1.  **Połączenie z WiFi**:

    - Program łączy się z siecią WiFi, używając wcześniej zdefiniowanego SSID i hasła.

2.  **Synchronizacja czasu z NTP**:

    - Po połączeniu z WiFi, mikrokontroler synchronizuje czas z serwerem NTP, aby mieć poprawny czas lokalny. Jest to wymagane do poprawnego działania połączenia z brokerem MQTT, który używa certyfikatu SSL.

3.  **Połączenie z brokerem MQTT**:

    - Program łączy się z brokerem MQTT, korzystając z bezpiecznego połączenia TLS. Uwierzytelnianie odbywa się za pomocą loginu i hasła.

4.  **Wyświetlanie wiadomości na LCD**:

    - Program odbiera wiadomości z subskrybowanego tematu MQTT i wyświetla je na ekranie LCD. Wiadomości są wyświetlane jeden znak po drugim.

#### Opis funkcji:

1.  **`connectToWiFi()`**: Łączy ESP8266 z siecią WiFi, próbując połączyć się, aż status WiFi będzie `WL_CONNECTED`.
2.  **`syncTime()`**: Synchronizuje czas z serwerem NTP, aby zapewnić poprawny czas dla SSL i bezpieczeństwa.
3.  **`connectToMQTT()`**: Łączy się z brokerem MQTT przy użyciu TLS (z weryfikacją certyfikatu).
4.  **`mqttCallback()`**: Przetwarza wiadomości otrzymane z subskrybowanego tematu i wyświetla je na LCD.
5.  **`loop()`**: Wykonuje się w pętli, sprawdzając, czy klient MQTT jest połączony. Jeśli nie, nawiązuje połączenie. Aktualizuje również MQTT i wyświetla wiadomości.

#### Instrukcje użytkowania:

1.  **Zainstaluj wymagane biblioteki**:

    - **ESP8266WiFi**: `ESP8266 Board Manager` w Arduino IDE.
    - **PubSubClient**: Zainstaluj za pomocą menedżera bibliotek w Arduino IDE.
    - **LiquidCrystal_I2C**: Zainstaluj za pomocą menedżera bibliotek.

2.  **Certyfikat SSL**:

    - Certyfikat SSL brokera EMQX został wbudowany w kod. Upewnij się, że masz poprawny certyfikat.

3.  **Uruchomienie**:

    - Wgraj kod na płytkę ESP8266 i monitoruj port szeregowy.

4.  **Monitorowanie**:

    - Wiadomości MQTT będą wyświetlane na ekranie LCD i w monitorze portu szeregowego.
