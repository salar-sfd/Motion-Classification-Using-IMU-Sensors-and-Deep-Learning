clc, clear, close all;

fs = 200;
spr = 100;
a = arduino('COM13', 'Uno');
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', spr);

%% Calibration
t0 = tic;
calibrationTimer = 2;
g_list = [];
while(toc(t0)<calibrationTimer)
    [accel, ~, ~] = read(imu);
    g_list = [g_list; vecnorm(accel, 2, 2)];
end
g = mean(g_list);

%% Data Aquisition
t0 = tic;
t1 = t0;
weight = 0.0;
N = 10;

color = ['r', 'g', 'b'];
axes = ['x', 'y', 'z'];
free_accel = [];
free_gyro = [];
figure;

for n = 1:N*5
    pause(1.5);

    if(mod(n, 5)==0)
        disp('Go!');
        disp(n/5);
        pause(0.1);

        [accel, gyro, mag] = read(imu);
        accel_vec = mean(accel)./norm(mean(accel));
        gyro_vec = mean(gyro);
        
        if(t1==t0)
            Down = -accel_vec;
            t1 = tic;
        else
            dt = toc(t1);
    
            teta = -mean(gyro).*dt;
            Down_gyro = RotateVector(Down, teta);
            Down_accel = -accel_vec;
            Down = Down_accel*weight + Down_gyro*(1-weight);

            t1 = tic;
        end
        if(norm(var(accel))<0.5)
            Down = -accel_vec;
        end
    
        Down = Down./norm(Down);
    
        free_accel = [free_accel; accel+g*Down];
        free_gyro = [free_gyro; gyro];
        hold off;
        for i=1:3
            subplot(3, 2, 2*i-1)
            plot(free_accel(:, i), "Color", color(i));
            xlim([1, spr]);
            ylim([-20, 20]);
            title(axes(i));
            hold off;
        end
        for i=1:3
            subplot(3, 2, 2*i)
            plot(free_gyro(:, i), "Color", color(i));
            xlim([1, spr]);
            ylim([-10, 10]);
            title(axes(i));
            hold off;
        end

    else
        disp('Ready?');
    end
end

%% Data Processing
x = reshape([free_gyro, free_accel], N, 6, spr);
figure
for i=1:N
    subplot(10, 2, i)
    s = normalize(reshape(x(i,:,:), 6, spr), 'norm', 2);
    imshow(s)
end
