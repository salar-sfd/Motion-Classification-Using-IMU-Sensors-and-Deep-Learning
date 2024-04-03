#include "MPU9250.h"
#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(10, 11);  // RX, TX pins

MPU9250 mpu;

void setup() {
    bluetoothSerial.begin(9600);
    Wire.begin();

    if (!mpu.setup(0x68)) {  // change to your own address
        while (1) {
            bluetoothSerial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
    }
}

void loop() {
    if (mpu.update()) {
        static uint32_t prev_ms = millis();
        if (millis() > prev_ms + 25) {
            print_roll_pitch_yaw();
            prev_ms = millis();
        }
    }
}

void print_roll_pitch_yaw() {
  String dataToSend = String(mpu.getAcc(0)*10, 5) + "," +
                  String(mpu.getAcc(1)*10, 5) + "," +
                  String(mpu.getAcc(2)*10, 5) + "," +
                  String(mpu.getGyro(0)*3.14159265359/180, 5) + "," +
                  String(mpu.getGyro(1)*3.14159265359/180, 5) + "," +
                  String(mpu.getGyro(2)*3.14159265359/180, 5);
                  // String(mpu.getMag(0), 5) + "," +
                  // String(mpu.getMag(1), 5) + "," +
                  // String(mpu.getMag(2), 5);

  bluetoothSerial.println(dataToSend);
}
