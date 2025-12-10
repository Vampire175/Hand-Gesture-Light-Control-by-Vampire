#include <BluetoothSerial.h>


BluetoothSerial SerialBT;
int ledPins[] = {13, 12, 14, 27, 26};  // Thumb, Index, Middle, Ring, Pinky

void setup() {
  Serial.begin(115200);  // Only one Serial.begin()
  SerialBT.begin("RoomMates AI");
  Serial.println("The device started, now you can pair it with Bluetooth!");
  
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  // Check if we have 5 bytes of finger data from Bluetooth
  if (SerialBT.available() >= 5) {
    for (int i = 0; i < 5; i++) {
      int fingerState = SerialBT.read();  // Read from Bluetooth
      digitalWrite(ledPins[i], fingerState == 1 ? HIGH : LOW);
    }
    Serial.println("Finger data received");  // Debug feedback
  }
  
  // Optional: Echo for debugging (comment out if not needed)
  /*
  if (SerialBT.available()) {
    char c = SerialBT.read();
    Serial.write(c);
  }
  */
}
