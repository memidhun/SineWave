#include "DHT.h"

#define DHTPIN 9      // Pin where the DHT11 is connected
#define DHTTYPE DHT11 // DHT11 sensor type

DHT dht(DHTPIN, DHTTYPE);

const int ledPin = 8;  // Pin for LED
const int fanPin = 6;  // Pin for Fan

void setup() {
  Serial.begin(9600);  // Begin serial communication
  dht.begin();         // Start DHT11 sensor
  pinMode(ledPin, OUTPUT); 
  pinMode(fanPin, OUTPUT);
}

void loop() {
  // Check if data is available from Python
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the command from serial
    if (command == '1') {
      digitalWrite(ledPin, !digitalRead(ledPin)); // Toggle LED
    } else if (command == '2') {
      digitalWrite(fanPin, !digitalRead(fanPin)); // Toggle Fan
    }
  }

  // Read temperature and humidity from DHT11 sensor
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Print temperature and humidity values
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print(" °C ");
    Serial.print("Humidity: ");
    Serial.print(hum);
    Serial.println(" %");
  }
  
  delay(2000); // Delay for sensor reading
}
