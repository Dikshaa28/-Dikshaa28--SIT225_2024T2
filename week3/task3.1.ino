#include "thingProperties.h"

const int trigPin = 9;
const int echoPin = 8;

void setup() {
  Serial.begin(9600);

  // Set up pins for HC-SR04
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Initialize cloud properties
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  // Update cloud variables
  ArduinoCloud.update();

  // Get distance and send to the cloud
  distance = getDistance();

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(1000);  // Send data every second
}

float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;  // Convert to centimeters
}

// Callback for distance change (required by Arduino Cloud)
void onDistanceChange() {
  // Currently empty since distance is updated directly in loop()
}


