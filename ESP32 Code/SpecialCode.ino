#include <BluetoothSerial.h>
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "AudioFileSourceSD.h"
#include "AudioOutputI2S.h"
#include "AudioGeneratorWAV.h"

BluetoothSerial SerialBT;

#define SD_CS 5  // SD card chip select pin

int ledPins[] = {13, 12, 15, 19, 10};

AudioGeneratorWAV *wav = nullptr;
AudioFileSourceSD *file = nullptr;
AudioOutputI2S *out = nullptr;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("RoomMates AI");
  
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }

  // Initialize SD card
  SPI.begin();
  if (!SD.begin(SD_CS)) {
    Serial.println("SD init failed");
    return;
  }
  Serial.println("SD OK");

  // Setup I2S audio output (GPIO 25, 26, 22 for DAC)
  out = new AudioOutputI2S();
  out->SetPinout(26, 25, 22); // BCLK, LRC, DIN
}

void playAudio(const char* filename) {
  // Stop previous playback
  if (wav && wav->isRunning()) {
    wav->stop();
    delete wav;
    delete file;
  }
  
  // Play new file
  file = new AudioFileSourceSD(filename);
  wav = new AudioGeneratorWAV();
  wav->begin(file, out);
}

void loop() {
  // Keep audio playing
  if (wav && wav->isRunning()) {
    if (!wav->loop()) wav->stop();
  }

  // Check for Bluetooth data
  if (SerialBT.available() >= 5) {
    int fingers[5];
    
    for (int i = 0; i < 5; i++) {
      fingers[i] = SerialBT.read();
      digitalWrite(ledPins[i], fingers[i] == 1 ? HIGH : LOW);
    }

    int thumb = fingers[0];
    int index = fingers[1];
    int middle = fingers[2];
    int ring = fingers[3];
    int pinky = fingers[4];

    // ONLY pinky raised → play music.wav
    if (pinky == 1 && thumb == 0 && index == 0 && middle == 0 && ring == 0) {
      playAudio("/washroom.wav");
      Serial.println("Playing washroom.wav");
    }

    // ONLY thumb raised → play something.wav
    if (thumb == 1 && index == 0 && middle == 0 && ring == 0 && pinky == 0) {
      playAudio("/water.wav");
      Serial.println("Playing water.wav");
    }
  }
}
