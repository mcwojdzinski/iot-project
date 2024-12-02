
## Opis ogólny

Projekt pozwala na rejestrację dźwięku z mikrofonu, jego zapis w pliku WAV, a następnie transkrypcję tego dźwięku na tekst za pomocą modelu Whisper. Po przetworzeniu tekstu, wynik jest publikowany na brokerze MQTT. System działa w pętli, umożliwiając ciągłe nagrywanie, transkrypcję i wysyłanie danych do serwera.

## Zależności

Aby uruchomić projekt, wymagane są następujące biblioteki:

-   `torch` – dla obsługi modelu Whisper, transkrypcji dźwięku.
-   `numpy` – do operacji na danych audio.
-   `scipy` – do zapisywania pliku WAV.
-   `sounddevice` – do nagrywania dźwięku.
-   `faster_whisper` – implementacja modelu Whisper.
-   `paho-mqtt` – do komunikacji z brokerem MQTT.
-   `unidecode` – do usuwania znaków diakrytycznych w transkrypcji.

Można je zainstalować za pomocą:

bash

Skopiuj kod

`pip install torch numpy scipy sounddevice paho-mqtt unidecode faster-whisper` 

## Parametry

### Parametry nagrywania audio

-   **SAMPLE_RATE** – częstotliwość próbkowania (domyślnie: `48000` Hz).
-   **CHANNELS** – liczba kanałów audio (domyślnie: 1, dla mono).

### Parametry MQTT

-   **broker** – adres brokera MQTT (domyślnie: `s3463711.ala.eu-central-1.emqxsl.com`).
-   **port** – port brokera (domyślnie: `8883`).
-   **topic** – temat MQTT, na który wysyłane będą wiadomości (domyślnie: `"cdv/trans"`).
-   **client_id** – identyfikator klienta MQTT, generowany losowo.
-   **username** – nazwa użytkownika do logowania się na brokerze (domyślnie: `espchinatest`).
-   **password** – hasło do logowania na brokerze (domyślnie: `"12345678%"`).

### Parametry modelu Whisper

-   **device** – urządzenie, na którym uruchamiany będzie model Whisper. Jeśli CUDA jest dostępna, używany jest GPU (`cuda`), w przeciwnym przypadku procesor CPU.
-   **model** – model Whisper (w tym przypadku: `"turbo"`).

### Parametry nagrywania dźwięku

-   **chunk_duration** – czas trwania każdego fragmentu nagrania (domyślnie: `5` sekund).

## Funkcje

### `list_audio_devices()`

Wyświetla dostępne urządzenia audio, które mogą służyć do nagrywania. Pokazuje identyfikator urządzenia oraz liczbę kanałów.

#### Parametry:

Brak.

#### Zwraca:

-   Listę dostępnych urządzeń audio.

### `select_audio_device()`

Pozwala użytkownikowi wybrać urządzenie do nagrywania z dostępnych urządzeń.

#### Parametry:

Brak.

#### Zwraca:

-   `device_id` – identyfikator wybranego urządzenia.

### `record_audio(duration: int)`

Nagrywa dźwięk przez określony czas (`duration`), używając domyślnego urządzenia audio.

#### Parametry:

-   **duration** – czas trwania nagrania w sekundach.

#### Zwraca:

-   Tablicę NumPy zawierającą dane audio.

### `save_audio_to_file(audio_data: np.ndarray, filename: str)`

Zapisuje dane audio do pliku WAV.

#### Parametry:

-   **audio_data** – dane audio w formacie NumPy.
-   **filename** – nazwa pliku, do którego zapisane będą dane audio.

#### Zwraca:

-   Brak (funkcja zapisuje plik audio).

### `connect_mqtt()`

Tworzy połączenie z brokerem MQTT, konfigurując odpowiednie dane logowania i ustawienia TLS.

#### Parametry:

Brak.

#### Zwraca:

-   Klienta MQTT, który będzie używany do publikowania wiadomości.

### `run()`

Główna funkcja uruchamiająca cały proces:

1.  Łączy się z brokerem MQTT.
2.  Nagrywa dźwięk przez 5 sekund (lub inną wartość zdefiniowaną w `chunk_duration`).
3.  Zapisuje nagranie audio do pliku WAV.
4.  Transkrybuje audio przy użyciu modelu Whisper.
5.  Publikuje transkrypcję na brokerze MQTT.

#### Parametry:

Brak.

#### Zwraca:

-   Brak (funkcja działa w nieskończonej pętli).

### `if __name__ == "__main__"`

Uruchamia funkcję `run()`, obsługując ewentualne wyjątki i błędy w trakcie działania programu.

## Przebieg działania

1.  **Uruchomienie skryptu**: Program zaczyna od sprawdzenia dostępności CUDA (jeśli jest dostępna, używa GPU, w przeciwnym razie CPU).
2.  **Nagrywanie**: Po nawiązaniu połączenia z brokerem MQTT, program zaczyna nagrywać dźwięk przez 5 sekund.
3.  **Zapis pliku WAV**: Nagranie jest zapisywane jako `temp.wav`.
4.  **Transkrypcja**: Plik WAV jest transkrybowany na tekst przez model Whisper.
5.  **Wysyłanie do MQTT**: Transkrypcja jest publikowana na brokerze MQTT, gdzie temat jest ustawiony na `"cdv/trans"`.
6.  **Powtarzanie procesu**: Proces nagrywania, transkrypcji i publikowania jest powtarzany w nieskończoność, co sekundę.

## Uwagi

-   Plik certyfikatu `emqxsl-ca.crt` musi być dostępny w katalogu, z którego uruchamiany jest program, jeśli połączenie z brokerem MQTT odbywa się za pomocą TLS.
-   Program nie obsługuje wielu urządzeń audio naraz, ale użytkownik może wybrać urządzenie, które chce używać do nagrywania.
-   Czas trwania nagrania (5 sekund) oraz częstotliwość nagrywania można dostosować, zmieniając zmienną `chunk_duration`.

## Przykład uruchomienia

bash

Skopiuj kod

`python audio_mqtt_transcription.py` 

Po uruchomieniu skryptu użytkownik zostanie poproszony o wybór urządzenia nagrywającego, po czym program zacznie nagrywać audio, transkrybować go i wysyłać wyniki do MQTT.
