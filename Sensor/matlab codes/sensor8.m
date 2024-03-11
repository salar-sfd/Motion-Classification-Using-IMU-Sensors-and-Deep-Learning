clc, clear, close all;

fs = 100;
spr = 5;
weight = 0.0;

a = arduino('COM13', 'Uno');
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', spr);

%% Calibration
calibrationTimer = 2;
g_list = [];
t0 = tic;
while(toc(t0)<calibrationTimer)
    [accel, ~, ~] = read(imu);
    g_list = [g_list; vecnorm(accel, 2, 2)];
end
g = mean(g_list);

%% Data Aquisition
t0 = tic;
t1 = t0;
tx = t0;
sample_time = 2;
relax_time = 4;
n_sample = sample_time*fs;
N = 8;
stopTimer = (sample_time+relax_time)*(N+1);
u = 1;

color = ['r', 'g', 'b'];
axes = ['x', 'y', 'z'];
free_accel = [];
free_gyro = [];
x = zeros(N, 6, n_sample);

disp('Ready?');
while(toc(t0) < stopTimer)
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

    if(toc(tx)>=4)
        disp('Go!');
    end

    if(toc(tx)>=4+sample_time && size(free_accel, 1)>=n_sample && size(free_accel, 1)>=n_sample)
        disp(u)
        disp('Stop!');
        x(u, :, :) = [free_accel(end-n_sample+1:end, :), free_gyro(end-n_sample+1:end, :)]';
        u = u+1;
        free_accel = [];
        free_gyro = [];
        tx = tic;
    end

end 
%%
figure
for i=1:N
    s = reshape(x(i, :, :), 6, []);
    subplot(8, 1, i)
%     plot(s')
%     legend('acc-x', 'acc-y', 'acc-z', 'gyr-x', 'gyr-y', 'gyr-z')
%     ylim([-10, 10]);
    imshow(s/10+0.5)
    colormap('default');
%     caxis([-1, 1]);
end