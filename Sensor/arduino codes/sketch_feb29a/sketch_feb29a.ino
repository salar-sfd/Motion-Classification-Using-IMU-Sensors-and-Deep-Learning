#include "MPU9250.h"

MPU9250 mpu; // You can also use MPU9255 as is


const unsigned long startMillis = 0;
void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);

    mpu.setup(0x68);  // change to your own address
    mpu.setAccelDataRate(1000);
    mpu.setGyroDataRate(1000);
}

void loop() {
    unsigned long currentMillis = millis();

    // Check if it's time to sample
    if (currentMillis - startMillis <=10000 && mpu.update()) {
        Serial.print(mpu.getAccX()); Serial.print(", ");
        Serial.print(mpu.getAccY()); Serial.print(", ");
        Serial.print(mpu.getAccZ()); Serial.print(", ");
        Serial.print(mpu.getGyroX()); Serial.print(", ");
        Serial.print(mpu.getGyroY()); Serial.print(", ");
        Serial.println(mpu.getGyroZ());
        
    }
}
//currentMillis - previousMillis >= samplingInterval && 
//        previousMillis = currentMillis;
//const unsigned long samplingInterval = 5; // Sampling interval in milliseconds
//unsigned long previousMillis = 0;
