#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SDA_PIN D6 /* Define the SDA pin here  */
#define SCL_PIN D7 /* Define the SCL Pin here */

LiquidCrystal_I2C lcd(0x27,16,2);  /* set the LCD address to 0x27 for a 16 chars and 2 line display */

// Definiowanie pinu dla komunikacji OneWire
const int temppin = 4;
int counter = 0;
// Ustawienie instancji komunikacji OneWire
OneWire oneWire(temppin);
// Ustawienie instancji dla sensora DS18B20
DallasTemperature sensors(&oneWire);
// WiFi credentials
const char *ssid = "";             // Replace with your WiFi name
const char *password = "";   // Replace with your WiFi password
// MQTT Broker settings
const int mqtt_port = 8883;  // MQTT port (TLS)
const char *mqtt_broker = "s3463711.ala.eu-central-1.emqxsl.com";  // EMQX broker endpoint


const char *temp_topic = "cdv/temp/sensor";
const char *video_topic = "cdv/aivideo";
const char *voice_topic =  "cdv/aivoice";


String video_text = "";
String voice_text = "";


const char *mqtt_username = "espchinatest";  // MQTT username for authentication
const char *mqtt_password = "12345678%";  // MQTT password for authentication
// NTP Server settings
const char *ntp_server = "pool.ntp.org";     // Default NTP server
// const char* ntp_server = "cn.pool.ntp.org"; // Recommended NTP server for users in China
const long gmt_offset_sec = 0;            // GMT offset in seconds (adjust for your time zone)
const int daylight_offset_sec = 0;        // Daylight saving time offset in seconds
// WiFi and MQTT client initialization
BearSSL::WiFiClientSecure espClient;
PubSubClient mqtt_client(espClient);
// SSL certificate for MQTT broker
// Load DigiCert Global Root G2, which is used by EMQX Public Broker: broker.emqx.io
static const char ca_cert[]
PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD
QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB
CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97
nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt
43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P
T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4
gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO
BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR
TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw
DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr
hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg
06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF
PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls
YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk
CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=
-----END CERTIFICATE-----
)EOF";
// Load DigiCert Global Root CA ca_cert, which is used by EMQX Serverless Deployment
/*
static const char ca_cert[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD
QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB
CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97
nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt
43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P
T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4
gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO
BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR
TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw
DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr
hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg
06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF
PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls
YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk
CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=
-----END CERTIFICATE-----
)EOF";
*/
// Function declarations
void connectToWiFi();
void connectToMQTT();
void syncTime();
void mqttCallback(char *topic, byte *payload, unsigned int length);

// Add these variables at the top with other global variables
int voice_scroll_position = 0;
int video_scroll_position = 0;
unsigned long last_scroll = 0;
const int SCROLL_DELAY = 300;  // Scroll speed in milliseconds
const int SCROLL_HOP = 2;

void setup() {
  Serial.begin(9600);
  sensors.begin();
  connectToWiFi();
  syncTime();  // X.509 validation requires synchronization time
  mqtt_client.setServer(mqtt_broker, mqtt_port);
  mqtt_client.setCallback(mqttCallback);
  connectToMQTT();
   
  Wire.begin(SDA_PIN, SCL_PIN);  /* Initialize I2C communication */
  lcd.init();                 /* initialize the lcd  */
  lcd.backlight();
  lcd.clear();

}
void connectToWiFi() {
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
     delay(1000);
     Serial.println("Connecting to WiFi...");
 }
 Serial.println("Connected to WiFi");
}
void syncTime() {
 configTime(gmt_offset_sec, daylight_offset_sec, ntp_server);
 Serial.print("Waiting for NTP time sync: ");
 while (time(nullptr) < 8 * 3600 * 2) {
     delay(1000);
     Serial.print(".");
 }
 Serial.println("Time synchronized");
 struct tm timeinfo;
 if (getLocalTime(&timeinfo)) {
     Serial.print("Current time: ");
     Serial.println(asctime(&timeinfo));
 } else {
     Serial.println("Failed to obtain local time");
 }
}
void connectToMQTT() {
 BearSSL::X509List serverTrustedCA(ca_cert);
 espClient.setTrustAnchors(&serverTrustedCA);
 while (!mqtt_client.connected()) {
     String client_id = "esp8266-client-" + String(WiFi.macAddress());
     Serial.printf("Connecting to MQTT Broker as %s.....\n", client_id.c_str());
     if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
         Serial.println("Connected to MQTT broker");
         mqtt_client.subscribe(video_topic);
         mqtt_client.subscribe(voice_topic);
         
     } else {
         char err_buf[128];
         espClient.getLastSSLError(err_buf, sizeof(err_buf));
         Serial.print("Failed to connect to MQTT broker, rc=");
         Serial.println(mqtt_client.state());
         Serial.print("SSL error: ");
         Serial.println(err_buf);
         delay(5000);
     }
 }
}


void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.print(topic);
    Serial.print("]: ");
    String message = "";


    for (int i = 0; i < length; i++) {
        message = message + (char) payload[i];
    }


    if (String(topic) == voice_topic) {
        voice_text = message;
        voice_scroll_position = 0;  // Reset scroll position for new message
    } else if (String(topic) == video_topic) {
        video_text = message;
        video_scroll_position = 0;  // Reset scroll position for new message
    }
}




void loop() {
  if (!mqtt_client.connected()) {
      connectToMQTT();
  }
  mqtt_client.loop();
  sensors.requestTemperatures();  // Żądanie odczytu temperatury
  // Odczyt temperatury w stopniach Celsjusza
  float temperatureC = sensors.getTempCByIndex(0);
  // Wyświetlanie wyniku w serial monitorze
  Serial.print(temperatureC);


  if (temperatureC != DEVICE_DISCONNECTED_C) {
      Serial.print("Temperatura: ");
      Serial.print(temperatureC);
      Serial.println("°C");
  } else {
      Serial.println("Sensor nie jest podłączony!");
  }

  const String data = "{\"temperature\": " + String(temperatureC) + ", \"humidity\": 55}";
  mqtt_client.publish(temp_topic, data.c_str());



  // Current time
  unsigned long current_time = millis();
  
  // Clear display and update both lines
  lcd.clear();
  
  // First line: voice text (scrolling if longer than 16 chars)
  lcd.setCursor(0,0);
  if(voice_text.length() > 16) {
      // Calculate the portion of text to display
      String voice_display = voice_text.substring(voice_scroll_position);
      if(voice_display.length() > 16) {
          voice_display = voice_display.substring(0, 16);
      }
      lcd.print(voice_display);
      
      // Update scroll position if enough time has passed
      if(current_time - last_scroll >= SCROLL_DELAY) {
          voice_scroll_position+=SCROLL_HOP;
          // Reset position when we reach the end
          if(voice_scroll_position >= voice_text.length()) {
              voice_scroll_position = 0;
          }
      }
  } else {
      lcd.print(voice_text);
  }
  
  // Second line: video text (scrolling if longer than 16 chars)
  lcd.setCursor(0,1);
  if(video_text.length() > 16) {
      // Calculate the portion of text to display
      String video_display = video_text.substring(video_scroll_position);
      if(video_display.length() > 16) {
          video_display = video_display.substring(0, 16);
      }
      lcd.print(video_display);
      
      // Update scroll position if enough time has passed
      if(current_time - last_scroll >= SCROLL_DELAY) {
          video_scroll_position+=SCROLL_HOP;
          // Reset position when we reach the end
          if(video_scroll_position >= video_text.length()) {
              video_scroll_position = 0;
          }
      }
  } else {
      lcd.print(video_text);
  }
  
  // Update last scroll time
  if(current_time - last_scroll >= SCROLL_DELAY) {
      last_scroll = current_time;
  }
  
  delay(50);  // Small delay to prevent display flickering
}
