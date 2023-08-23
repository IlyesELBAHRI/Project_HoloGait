/*
 * Author: Louis Dubarle
 * For : Cereneo Foundation
 * File: vibrate.ino
 * Project : Research project on the use of haptic feedback for Parkinson's
 * disease patients with Freezing of Gait (FOG)
 *
 * Commands available:
 * V <float:frequency> : Vibrates the whole system at a given frequency
 *
 * T <int:id_tactor> <float:frequency> : Vibrates the given tactor at a given
 * frequency
 *
 * S : Stops all vibrations
 */

#include <Arduino.h>
#include <FastLED.h>
#include <WiFi.h>
#include <WiFiUdp.h>

#define BAT A13
#define BUTTON 38
#define LED 0
#define TIME_SHOWN 2500

#define REG A5
#define T0 33
#define T1 27
#define T2 13
#define T3 12

#define LONG_PRESS 3000

#define LOW_BAT_SLEEP_S 10
#define LOW_BAT 10

CRGB led[1];
bool led_on = false;
unsigned long last_show = 0;

bool button_pressed = false;
bool button_released = false;
unsigned long time_pressed = 0;

// WiFi credentials
const char *ssid = "ZyXELD72BD8";
const char *password = "B3EBEC29B5148";

// UDP server
WiFiUDP udp;
const int port = 8080;
char received[256];

int vibrating_0 = 0;
int vibrating_1 = 0;
int vibrating_2 = 0;
int vibrating_3 = 0;
int delay_ms = 0;

unsigned long last_millis = 0;

int battery_level();

void battery_led();

void handle_led();

void IRAM_ATTR on_press();

void handle_button();

void on_receive();

void activate_tactor_0();
void activate_tactor_1();
void activate_tactor_2();
void activate_tactor_3();
void stop_all_tactors();

void setup() {
    Serial.begin(115200);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to WiFi");

    Serial.println("Listening on port " + String(port));
    udp.begin(port);

    Serial.println("MAC address " + WiFi.macAddress());
    Serial.println("Send commands to " + WiFi.localIP().toString());

    FastLED.addLeds<WS2812B, LED, GRB>(led, 1);
    FastLED.setBrightness(25);

    pinMode(BUTTON, INPUT_PULLUP);
    attachInterrupt(BUTTON, on_press, CHANGE);

    pinMode(REG, OUTPUT);
    pinMode(T0, OUTPUT);
    pinMode(T1, OUTPUT);
    pinMode(T2, OUTPUT);
    pinMode(T3, OUTPUT);

    digitalWrite(REG, HIGH);
    digitalWrite(T0, LOW);
    digitalWrite(T1, LOW);
    digitalWrite(T2, LOW);
    digitalWrite(T3, LOW);
}

void loop() {
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }

    if (udp.parsePacket()) on_receive();

    if (button_pressed) handle_button();

    if (led_on) handle_led();

    battery_level();

    vibrating_0 ? activate_tactor_0() : digitalWrite(T0, LOW);
    vibrating_1 ? activate_tactor_1() : digitalWrite(T1, LOW);
    vibrating_2 ? activate_tactor_2() : digitalWrite(T2, LOW);
    vibrating_3 ? activate_tactor_3() : digitalWrite(T3, LOW);

    delay(10);
}

int battery_level() {
    float meas = analogReadMilliVolts(BAT);
    meas *= 2;
    meas /= 1000;
    meas = (meas - 3.0) * 100 / (4.35 - 3.0);

    while (meas < LOW_BAT) {
        digitalWrite(REG, LOW);
        digitalWrite(T0, LOW);
        digitalWrite(T1, LOW);
        digitalWrite(T2, LOW);
        digitalWrite(T3, LOW);
        esp_deep_sleep(LOW_BAT_SLEEP_S * 1000000);
    }

    return meas;
}

void battery_led() {
    int level = battery_level();
    if (level > 75) {
        led[0] = CRGB::Green;
    } else if (level > 50) {
        led[0] = CRGB::Yellow;
    } else if (level > 25) {
        led[0] = CRGB::Orange;
    } else {
        led[0] = CRGB::Red;
    }
    FastLED.show();
    led_on = true;
}

void handle_led() {
    if (millis() - last_show > TIME_SHOWN) {
        led_on = false;
        led[0] = CRGB::Black;
        FastLED.show();
    }
}

void IRAM_ATTR on_press() {
    if (button_pressed) {
        button_released = true;
        return;
    } else {
        button_pressed = true;
        time_pressed = millis();
    }
}

void handle_button() {
    if (button_released) {
        button_released = false;
        button_pressed = false;
        time_pressed = millis() - time_pressed;
        if (time_pressed > LONG_PRESS) {
            digitalWrite(REG, LOW);
            digitalWrite(T0, LOW);
            digitalWrite(T1, LOW);
            digitalWrite(T2, LOW);
            digitalWrite(T3, LOW);
            esp_deep_sleep_start();
        } else {
            last_show = millis();
            battery_led();
        }
    }
}

void on_receive() {
    udp.read(received, 256);
    Serial.println(received);
    char command = received[0];
    switch (command) {
        case 'V': {
            float frequency = atof(&received[2]);

            if (!frequency)
                delay_ms = 0;
            else
                delay_ms = (int)1000 / frequency;

            last_millis = millis();
            vibrating_0 = 1;
            vibrating_1 = 1;
            vibrating_2 = 1;
            vibrating_3 = 1;
            break;
        }

        case 'T': {
            char *arg;
            float argv[4];
            int argc = 0;

            arg = strtok(received, " ");
            arg = strtok(NULL, " ");
            while (arg) {
                argv[argc++] = atof(arg);
                arg = strtok(NULL, " ");
            }

            float frequency = argv[argc - 1];

            if (!frequency)
                delay_ms = 0;
            else
                delay_ms = (int)1000 / frequency;

            for (int i = 0; i < argc - 1; i++) {
                switch ((int)argv[i]) {
                    case 0:
                        vibrating_0 = 1;
                        vibrating_1 = 0;
                        vibrating_2 = 0;
                        vibrating_3 = 0;
                        break;

                    case 1:
                        vibrating_0 = 0;
                        vibrating_1 = 1;
                        vibrating_2 = 0;
                        vibrating_3 = 0;
                        break;

                    case 2:
                        vibrating_0 = 0;
                        vibrating_1 = 0;
                        vibrating_2 = 1;
                        vibrating_3 = 0;
                        break;

                    case 3:
                        vibrating_0 = 0;
                        vibrating_1 = 0;
                        vibrating_2 = 0;
                        vibrating_3 = 1;
                        break;

                    default:
                        vibrating_0 = 0;
                        vibrating_1 = 0;
                        vibrating_2 = 0;
                        vibrating_3 = 0;
                        break;
                }
            }

            last_millis = millis();
            break;
        }

        case 'S': {
            stop_all_tactors();
            break;
        }

        default: {
            Serial.println("Invalid command");
            break;
        }
    }
}

void activate_tactor_0() {
    if (millis() - last_millis <= delay_ms / 4)
        digitalWrite(T0, HIGH);
    else if ((millis() - last_millis <= delay_ms))
        digitalWrite(T0, LOW);
    else
        last_millis = millis();
}

void activate_tactor_1() {
    if (millis() - last_millis <= delay_ms / 4)
        digitalWrite(T1, HIGH);
    else if ((millis() - last_millis <= delay_ms))
        digitalWrite(T1, LOW);
    else
        last_millis = millis();
}

void activate_tactor_2() {
    if (millis() - last_millis <= delay_ms / 4)
        digitalWrite(T2, HIGH);
    else if ((millis() - last_millis <= delay_ms))
        digitalWrite(T2, LOW);
    else
        last_millis = millis();
}

void activate_tactor_3() {
    if (millis() - last_millis <= delay_ms / 4)
        digitalWrite(T3, HIGH);
    else if ((millis() - last_millis <= delay_ms))
        digitalWrite(T3, LOW);
    else
        last_millis = millis();
}

void stop_all_tactors() {
    vibrating_0 = 0;
    vibrating_1 = 0;
    vibrating_2 = 0;
    vibrating_3 = 0;
    digitalWrite(T0, LOW);
    digitalWrite(T1, LOW);
    digitalWrite(T2, LOW);
    digitalWrite(T3, LOW);
}