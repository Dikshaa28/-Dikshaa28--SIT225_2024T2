#include "thingProperties.h"  // Include Arduino IoT Cloud properties
#include <WiFiNINA.h>         // Include Wi-Fi library

#define TRIG_PIN 9
#define ECHO_PIN 10
#define THRESHOLD_DISTANCE 10  // Threshold in cm

// Wi-Fi credentials
const char* ssid = "OPPO A15S";         // Replace with your Wi-Fi SSID
const char* password = "devanshi1234"; // Replace with your Wi-Fi password

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    // Connect to Wi-Fi
    Serial.println("Connecting to WiFi...");
    int status = WiFi.begin(ssid, password);
    
    // Wait until Wi-Fi is connected
    while (status != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
        status = WiFi.begin(ssid, password);
    }

    Serial.println("\nConnected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Initialize Arduino Cloud connection
    initProperties();
    ArduinoCloud.begin(ArduinoIoTPreferredConnection);
}
void loop() {
    ArduinoCloud.update();  // Sync with IoT Cloud

    distance = measureDistance();  // Get distance from sensor

    Serial.print("Distance: ");
    Serial.println(distance);

    if (distance < THRESHOLD_DISTANCE) {
        alarm = true;  // Trigger alarm in the cloud
    } else {
        alarm = false;  // Reset alarm if distance is safe
    }

    delay(1000);  // Wait before taking the next reading
}

// Function to measure distance using HC-SR04
float measureDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    return duration * 0.034 / 2;  // Convert time to cm
}

// IoT Cloud Callbacks
void onDistanceChange() {
    // This function is required by Arduino IoT Cloud but can be left empty
}

void onAlarmChange() {
    // This function is required by Arduino IoT Cloud but can be left empty
}
