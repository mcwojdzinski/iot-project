# Projekt IOT

## Autorzy

1. Bogusz Krzyżanowski, 28667
2. Mateusz Cwojdziński, 28927

## Główna dokumentacja
* [Arduino](https://github.com/mcwojdzinski/iot-project/blob/main/fullintegration-arduino.md) - Dokumentacja dla arduino
* [Python](https://github.com/mcwojdzinski/iot-project/blob/main/fullintegration-python.md) - Dokumentacja dla python'a

#### Schematy blokowe zrobione w mermaid chart
* [Python](https://www.mermaidchart.com/raw/828bfac8-1771-4ef8-a076-39dbcde36b54?theme=light&version=v0.1&format=svg)
* [Arduino](https://www.mermaidchart.com/raw/ddef788c-7891-4dcb-90a3-3b521e712d67?theme=light&version=v0.1&format=svg)

## Dokumentacja dla poszczególnych programów:

### ESP8266

* [ESP8266](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/extra/esp8266.md) - Dokumentacja programu w arduino do mierzenia temperatury
* [Subscriber](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/extra/subscriber.md) - Dokumentacja programu w pythonie wsyłająca dane z arduino do influxDB i wyświetlana w grafanie

### Speech-to-text

* [Speech-to-text-python](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/extra/speech-to-text-python.md) - Program uzywajacy modelu do tlumaczenia mowy na tekst
* [Speech-to-text-arduino](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/extra/speech-to-text-arduino.md) - Pobieranie z MQTT tekstu i wyswietlanie na ekranie LCD

### Video-to-text

* [Video to text arduino](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/extra/video-to-text-arduino.md) - Dokumentacja dla wyświetlania obiektów z modelu yolo na wyświetlaczu lcd
* [Video to text python](https://github.com/mcwojdzinski/mqtt-temperature/blob/main/extra/video-to-text-python.md) - Dokumentacja programu wykorzystująca model yolo do wykrywania obiektów z kamery
