clc, clear, close all;
if(exist('bt', 'var') == 0)
    bt = bluetooth('MPU9250'); 
end
disp('Connected.')

accel_list = [];
gyro_list = [];
t_list = [];
color = ['r', 'g', 'b'];
acc_axes = {'acc-x', 'acc-y', 'acc-z'};
gyr_axes = {'gyr-x', 'gyr-y', 'gyr-z'};

fopen(bt);
q=0;
t0 = tic;
flushinput(bt);
while toc(t0)<60
    data = fgetl(bt);
    value = cellfun(@str2double, split(data, ",")).';
    accel = value(1:3)/2000;
    gyro = value(4:6)/3000;
    t = value(7)/1000;

    accel_list = [accel_list; accel];
    gyro_list = [gyro_list; gyro];
    t_list = [t_list, t];

    hold off;
    if(mod(q, 21)==0)
    for i=1:3
        subplot(3, 2, 2*i-1)
        plot(accel_list(:, i), "Color", color(i));
        if(length(accel_list)-500>0)
            xlim([length(accel_list)-500, length(accel_list)])
        end
        ylim([-20, 20]);
        title(acc_axes{i});
        hold on;
    end
    for i=1:3
        subplot(3, 2, 2*i)
        plot(gyro_list(:, i), "Color", color(i));
        if(length(gyro_list)-500>0)
            xlim([length(gyro_list)-500, length(gyro_list)])
        end
        ylim([-20, 20]);
        title(gyr_axes{i});
        hold on;
    end
    pause(0.0001);
    flushinput(bt);
    end
    q=q+1;
end

%%
figure
hold off;
for i=1:3
subplot(3, 2, 2*i-1)
plot(t_list, accel_list(:, i), "Color", color(i));
%         xlim([0, 100])
ylim([-30, 30]);
title(acc_axes{i});
hold on;
end
for i=1:3
subplot(3, 2, 2*i)
plot(t_list, gyro_list(:, i), "Color", color(i));
%         xlim([0, 100])
ylim([-30, 30]);
title(gyr_axes{i});
hold on;
end

%%
figure
hold off;
for i=1:3
subplot(3, 2, 2*i-1)
plot(abs(fft(accel_list(:, i))), "Color", color(i));
title(acc_axes{i});
hold on;
end
for i=1:3
subplot(3, 2, 2*i)
plot(abs(fft(gyro_list(:, i))), "Color", color(i));
title(gyr_axes{i});
hold on;
end
