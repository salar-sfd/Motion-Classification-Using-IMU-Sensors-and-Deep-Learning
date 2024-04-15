%% Connection
clc, clear, close all;
if(exist('bt', 'var') == 0)
    bt = bluetooth('MPU9250'); 
end
disp('Connected.')

%% Calibration
calibrationTimer = 2;
accel_list = [];
gyro_list = [];
t_list = [];
t0 = tic;
disp('Calibrating...');
while(toc(t0)<calibrationTimer)
    data = fgetl(bt);
    value = cellfun(@str2double, split(data, ",")).';
    accel = value(1:3)/(16384);
    gyro = value(4:6)/(131*180/pi);
    t = value(7)/1000;
    
    accel_list = [accel_list; accel];
    gyro_list = [gyro_list; gyro];
    t_list = [t_list, t];
end
accel_var = var(accel_list);

gyro_var = var(gyro_list);
gyro_bias = mean(gyro_list);


gyro_list = gyro_list - gyro_bias;

disp('Calibration finished.');

%% Data Acindexuisition
flag_list = [];
color = ['r', 'g', 'b'];
acc_axes = {'acc-x', 'acc-y', 'acc-z'};
gyr_axes = {'gyr-x', 'gyr-y', 'gyr-z'};
window_size = 15;
spr = 5;
fopen(bt);
index=0;
threshold = 100*accel_var;
flushinput(bt);
t0 = tic;
while toc(t0)<20
    %
    for i=1:spr
        data = fgetl(bt);
        value = cellfun(@str2double, split(data, ",")).';
        accel = value(1:3)/(16384);
        gyro = value(4:6)/(131*180/pi) - gyro_bias;
        t = value(7)/1000;
        
        accel_list = [accel_list; accel];
        gyro_list = [gyro_list; gyro];
        t_list = [t_list, t];
        index=index+1;
    end
    %
    
    %
    if(all(var(accel_list(end-window_size+1:end, :))>threshold))
        disp(1);
        flag_list = [flag_list, 1];
        threshold = 30*accel_var;
    else
        disp(0);
        flag_list = [flag_list, 0];
        threshold = 50*accel_var;
    end
    %

    pause(0.0001);
    flushinput(bt);
end