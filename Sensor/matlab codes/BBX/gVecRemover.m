%% Connection
clc, clear, close all;
if(exist('bt', 'var') == 0)
    bt = bluetooth('MPU9250'); 
end
disp('Connected.')

%% Calibration
calibrationTimer = 2;
accel_raw_list = [];
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
g_vec = mean(accel_list);
gyro_bias = mean(gyro_list);
accel_var = var(accel_list);
gyro_var = var(gyro_list);

accel_raw_list = accel_list;
accel_list = accel_list - g_vec;
gyro_list = gyro_list - gyro_bias;

disp('Calibration finished.');

%% Data Acindexuisition
color = ['r', 'g', 'b'];
acc_axes = {'acc-x', 'acc-y', 'acc-z'};
gyr_axes = {'gyr-x', 'gyr-y', 'gyr-z'};
window_size = 60;
spr = 10;
fopen(bt);
index=0;
flushinput(bt);
t0 = tic;
while toc(t0)<10
    %
    for i=1:spr
    data = fgetl(bt);
    value = cellfun(@str2double, split(data, ",")).';
    accel_raw = value(1:3)/(16384);
    gyro = value(4:6)/(131*180/pi) - gyro_bias;
    t = value(7)/1000;
    
    accel_raw_list = [accel_raw_list; accel_raw];
    gyro_list = [gyro_list; gyro];
    t_list = [t_list, t];
    end
    %
    
    %
    if(all(var(accel_raw_list(end-window_size+1:end, :))<30*accel_var))
        g_vec = mean(accel_raw_list(end-spr+1:end, :));
    else
        dt = t_list(end-spr+1:end)-t_list(end-spr:end-1);
        teta = sum(-gyro_list(end-spr+1:end, :).*dt');
        g_vec = RotateVector(g_vec, teta);
    end
    
    %

    %
%     g_n = g_vec/norm(g_vec);
%     quiver3(0, 0, 0, g_n(1), g_n(2), g_n(3), 'LineWidth', 2);
%     axis equal;
%     xlim([-1, 1]);
%     ylim([-1, 1]);
%     zlim([-1, 1]);
%     xlabel('x');
%     ylabel('y')
%     zlabel('z')
    %

    %
    hold off;
    if(mod(index, 2)==0)
    for i=1:3
        subplot(3, 2, 2*i-1)
        plot(accel_list(:, i), "Color", color(i));
        if(length(accel_list)-500>0)
            xlim([length(accel_list)-500, length(accel_list)])
        end
        ylim([-2, 2]);
        title(acc_axes{i});
        hold on;
    end
    for i=1:3
        subplot(3, 2, 2*i)
        plot(gyro_list(:, i), "Color", color(i));
        if(length(gyro_list)-500>0)
            xlim([length(gyro_list)-500, length(gyro_list)])
        end
        ylim([-2*pi, 2*pi]);
        title(gyr_axes{i});
        hold on;
    end
    end
    %

    pause(0.0001);
    flushinput(bt);
    index=index+1;
end