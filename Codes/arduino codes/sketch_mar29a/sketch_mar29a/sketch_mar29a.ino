#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(10, 11);  // RX, TX pins for HC-05 Bluetooth module
int en_pin = 9;

void setup() {
  Serial.begin(38400);           // Serial monitor baud rate
  bluetoothSerial.begin(38400); // HC-05 baud rate
}

void loop() {
  if (bluetoothSerial.available()) {
    char response = bluetoothSerial.read();
    Serial.write(response);
  }
  
  if (Serial.available()) {
    char cmd = Serial.read();
    bluetoothSerial.write(cmd);
  }
}
