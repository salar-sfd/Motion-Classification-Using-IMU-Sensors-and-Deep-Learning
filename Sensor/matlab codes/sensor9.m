clc, clear, close all;

fs = 200;
spr = 3;
weight = 0.2;

a = arduino('COM13', 'Uno');
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', spr);

%% Calibration
calibrationTimer = 5;
g_list = [];
gyro_list = [];
t0 = tic;
while(toc(t0)<calibrationTimer)
    [accel, gyro, ~] = read(imu);
    g_list = [g_list; vecnorm(accel, 2, 2)];
    gyro_list = [gyro_list; gyro];
end
g = mean(g_list);
gyro_bias = mean(gyro_list);

%% Data Aquisition
t0 = tic;
t1 = t0;
tx = t0;
sample_time = 2;
relax_time = 4;
n_sample = sample_time*fs;
N = 8;
% stopTimer = (sample_time+relax_time)*(N+1);
stopTimer = 600;
u = 1;

color = ['r', 'g', 'b'];
axes = ['x', 'y', 'z'];
free_accel = [];
free_gyro = [];
v = [0, 0];
x = [0, 0];

disp('Ready?');
while(toc(t0) < stopTimer)
    [accel, gyro, mag] = read(imu);
    
    gyro = gyro - gyro_bias;
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

%     if(toc(tx)>=4)
%         disp('Go!');
%     end
% 
%     if(toc(tx)>=4+sample_time && size(free_accel, 1)>=n_sample && size(free_accel, 1)>=n_sample)
%         disp(u)
%         disp('Stop!');
%         x(u, :, :) = [free_accel(end-n_sample+1:end, :), free_gyro(end-n_sample+1:end, :)]';
%         u = u+1;
%         free_accel = [];
%         free_gyro = [];
%         tx = tic;
%     end
    dt = toc(tx);
    tx = tic;
    x = x - mean(free_gyro(end-spr+1:end, [3,2]))*dt;
%     v = v*exp(-0.1);
%     x = x + v*dt;

    if(x(1)>1)
        v=v*0;
        x(1)=1;
    end
    if(x(1)<-1)
        v=v*0;
        x(1)=-1; 
    end
    if(x(2)>1)
        v=v*0;
        x(2)=1;
    end
    if(x(2)<-1)
        v=v*0;
        x(2)=-1; 
    end


    scatter(x(1)*20, x(2)*20, 'filled', 'Color', 'r');
    xlim([-5, 5])
    ylim([-5, 5])
    hold off;
    pause(0.01);
    
end 