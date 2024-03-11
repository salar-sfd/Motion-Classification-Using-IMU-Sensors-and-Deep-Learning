clc, clear, close all;

a = arduino('COM13', 'Uno');

fs = 200;
weight = 0.0;
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', 20);
t0 = tic;
stopTimer = 10; 
figure;

A = [];
G = [];
M = [];

while(toc(t0) < stopTimer) 
    [accel, gyro, mag] = read(imu);
    A = [A; accel];
    G = [G; gyro];
    M = [M; mag];
end 

