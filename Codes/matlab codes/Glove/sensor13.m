%% Connecting Arduino
clc, clear, close all;

fs = 100;
spr = 1;

disp('Connecting...');
a = arduino('COM13', 'Uno');
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', spr);
disp('Connected.');

%% Calibration
calibrationTimer = 5;
g_list = [];
gyro_list = [];
t0 = tic;
disp('Calibrating...');
while(toc(t0)<calibrationTimer)
    [accel, gyro, ~] = read(imu);
    g_list = [g_list; vecnorm(accel, 2, 2)];
    gyro_list = [gyro_list; gyro];
end
g = mean(g_list);
gyro_bias = mean(gyro_list);

disp('Calibration finished.');

%% Data Aquisition
weight = 0.1;
t0 = tic;
t1 = t0;
stopTimer = 120;

color = ['r', 'g', 'b'];
axes = ['x', 'y', 'z'];

n = 1;
x = [];
y = [0, 0];
accel_list = [];
accel_list_depth = 20;
disp('Data Aquisition...');
figure
while(toc(t0) < stopTimer)

    [accel, gyro, mag] = read(imu);
    accel_list = [accel_list; accel];
    gyro = gyro - gyro_bias;
    pointer = (get(0, 'PointerLocation'));


    x = [x; [accel, gyro]];
    if(size(x, 1) > 64)
        y = y + (std_y .* predict(net, x(end-64+1:end, :)')+mu_y)*5;
        scatter(y(1), y(2));
        ylim([-5, 5])
        xlim([-5, 5])
        pause(0.01)
    end
    
    n = n+1;
end
