#include <DHT.h>

#define DHTPIN 3       
#define DHTPOWER 4   
#define DHTGROUND 2    
#define LEDPIN 13      
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  pinMode(DHTPOWER, OUTPUT);
  pinMode(DHTGROUND, OUTPUT);
  digitalWrite(DHTPOWER, HIGH);
  digitalWrite(DHTGROUND, LOW);
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, LOW);
  dht.begin();
}

void loop() {
  static unsigned long lastRead = 0;
  if (millis() - lastRead >= 2000) {
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    if (!isnan(temp) && !isnan(hum)) {
      Serial.print("{\"temperature\":");
      Serial.print(temp);
      Serial.print(",\"humidity\":");
      Serial.print(hum);
      Serial.println("}");
    }
    lastRead = millis();
  }

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "{\"led\":\"ON\"}") {
      digitalWrite(LEDPIN, HIGH);
    } else if (command == "{\"led\":\"OFF\"}") {
      digitalWrite(LEDPIN, LOW);
    }
  }
}