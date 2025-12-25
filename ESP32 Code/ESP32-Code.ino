#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

int ledPins[] = {13, 12};      
int speakerPins[] = {26, 25};  

const char *pin = "1234";  // Your PIN

void setup() {
  Serial.begin(115200);
  
  // IMPORTANT: setPin() MUST come BEFORE begin()
  SerialBT.setPin(pin, strlen(pin));  // Correct syntax: (pin_string, length)
  SerialBT.begin("RoomMates AI");
  
  for (int i = 0; i < 2; i++) pinMode(ledPins[i], OUTPUT);
  for (int i = 0; i < 2; i++) pinMode(speakerPins[i], OUTPUT);
  
  Serial.println("Bluetooth Ready with PIN");
}

void loop() {
  if (SerialBT.available() >= 5) {
    byte led1_index = SerialBT.read();
    byte led2_middle = SerialBT.read();
    byte speaker1_pinky = SerialBT.read();
    byte speaker2_thumb = SerialBT.read();
    byte reserved = SerialBT.read();
    
    digitalWrite(ledPins[0], led1_index ? HIGH : LOW);
    digitalWrite(ledPins[1], led2_middle ? HIGH : LOW);
    digitalWrite(speakerPins[0], speaker1_pinky ? HIGH : LOW);
    digitalWrite(speakerPins[1], speaker2_thumb ? HIGH : LOW);
    
    Serial.print("Received - LED1:");
    Serial.print(led1_index);
    Serial.print(" LED2:");
    Serial.print(led2_middle);
    Serial.print(" SPK1:");
    Serial.print(speaker1_pinky);
    Serial.print(" SPK2:");
    Serial.println(speaker2_thumb);
  }
}
