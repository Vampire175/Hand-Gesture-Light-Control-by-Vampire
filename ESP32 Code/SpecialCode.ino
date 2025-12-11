#include <BluetoothSerial.h>
#include <SD.h>
#include <TMRpcm.h>
#include <SPI.h>

BluetoothSerial SerialBT;
TMRpcm tmrpcm;

#define SD_ChipSelectPin 5        // <-- set your SD CS pin here

int ledPins[] = {13, 12, 15, 19, 10}; // 0:Thumb 1:Index 2:Middle 3:Ring 4:Pinky

void setup() {
  Serial.begin(9600);
  SerialBT.begin("RoomMates AI");

  tmrpcm.speakerPin = 14;        // PWM‑capable pin for audio out[web:14]

  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  if (!SD.begin(SD_ChipSelectPin)) {
    Serial.println("SD fail");
    return;
  } else {
    Serial.println("SD ok");
  }
}

void loop() {
  // Wait until we have 5 bytes from Android
  if (SerialBT.available() >= 5) {
    int fingers[5];

    for (int i = 0; i < 5; i++) {
      fingers[i] = SerialBT.read();   // 0 or 1
      digitalWrite(ledPins[i], fingers[i] == 1 ? HIGH : LOW);
    }

    int thumb = fingers[0];  // make sure Android sends in this order
    int index = fingers[1];
    int middle = fingers[2];
    int ring = fingers[3];
    int pinky = fingers[4];

    // ONLY pinky = 1 -> play washroom.wav
    if (pinky == 1 && thumb == 0 && index == 0 && middle == 0 && ring == 0) {
      tmrpcm.play("washroom.wav");      // file on SD root, 8‑bit mono WAV[web:20]
    }

    // ONLY thumb = 1 -> play water.wav
    if (thumb == 1 && index == 0 && middle == 0 && ring == 0 && pinky == 0) {
      tmrpcm.play("water.wav");
    }
  }
}
