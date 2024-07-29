clc, clear;
a = arduino('COM54', 'Uno');

fs = 100;
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix');

ts = tic; 
stopTimer = 50; 
magReadings=[]; 
while(toc(ts) < stopTimer) 
    % Rotate the sensor along x axis from 0 to 360 degree. 
    % Take 2-3 rotations to improve accuracy. 
    % For other axes, rotate along that axes. 
   [accel,gyro,mag] = read(imu); 
   magReadings = [magReadings;mag]; 
end 

[A, b] = magcal(magReadings); % A = 3x3 matrix for soft iron correction 
                              % b = 3x1 vector for hard iron correction 