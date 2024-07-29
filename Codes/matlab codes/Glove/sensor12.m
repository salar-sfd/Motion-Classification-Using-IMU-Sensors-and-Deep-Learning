%% c
%% Connecting Arduino
clc, clear, close all;

screen_size = get(0, 'ScreenSize');

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
stopTimer = 40;

color = ['r', 'g', 'b'];
axes = ['x', 'y', 'z'];

n = 1;
x = [];
y = [];
accel_list = [];
accel_list_depth = 20;
disp('Data Aquisition...');
while(toc(t0) < stopTimer)
    if(mod(n,10)==0)
        disp(toc(t0))
    end

    [accel, gyro, mag] = read(imu);
    accel_list = [accel_list; accel];
    gyro = gyro - gyro_bias;
    pointer = (get(0, 'PointerLocation'));


    x = [x; [accel, gyro]];
    y = [y; [pointer(1)/screen_size(3), pointer(2)/screen_size(4)]];
    
    n = n+1;
end
disp('Data Aquisition Finished.')

%% Plotting
subplot(1, 2, 1);
scatter(y(:, 1), y(:, 2), 'filled');
subplot(1, 2, 2);
plot(x(:, 1:6));

%% Processing
x = x(1:end-1, :);
y = y(2:end, :)-y(1:end-1, :);

%% Saving
save('..\datasets\eval2', 'x', 'y');