// MPU-6050 Short Example Sketch
// By Arduino User JohnChi
// August 17, 2014
// Public Domain
#include<Wire.h>
const int MPU_addr = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

unsigned long start, now, last;
unsigned int loops = 0;
void setup() {
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x1B);  // PWR_MGMT_1 register
  Wire.write(0x10);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(115200);
  last = millis();
  start = last;
}

void loop() {
//  if(millis()-start<=10000)
//  {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14); // request a total of 14 registers
  int t = Wire.read();
  AcX = (t << 8) | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  t = Wire.read();
  AcY = (t << 8) | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  t = Wire.read();
  AcZ = (t << 8) | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  
  t = Wire.read(); t = Wire.read();
//    Tmp = (t << 8) | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)

  t = Wire.read();
  GyX = (t << 8) | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  t = Wire.read();
  GyY = (t << 8) | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  t = Wire.read();
  GyZ = (t << 8) | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  t = Wire.read();
  loops++;
  now = millis();
  if (now - last > 5UL) {
    Serial.print(AcX);
    Serial.print(", "); Serial.print(AcY);
    Serial.print(", "); Serial.print(AcZ);
    Serial.print(", "); Serial.print(GyX);
    Serial.print(", "); Serial.print(GyY);
    Serial.print(", "); Serial.print(GyZ);
    Serial.print(", "); Serial.println(now);
//    Serial.print(", "); Serial.println(loops);
    loops = 0;
    last = now;
  }
//}
}
