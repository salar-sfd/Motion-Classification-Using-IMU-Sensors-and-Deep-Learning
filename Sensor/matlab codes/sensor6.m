clc, clear, close all;

fs = 200;
weight = 0.0;

a = arduino('COM13', 'Uno');
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', 10);

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
color = ['r', 'g', 'b'];
acc_axes = {'acc-x', 'acc-y', 'acc-z'};
gyr_axes = {'gyr-x', 'gyr-y', 'gyr-z'};

t0 = tic;
t1 = t0;
tx = tic;
stopTimer = 400;
free_accel = [];
free_gyro = [];
figure;

while(toc(t0) < stopTimer) 
    [accel, gyro, mag] = read(imu);

    accel_vec = mean(accel)./norm(mean(accel));
    gyro_vec = mean(gyro);
    mag_vec = mean(mag)./norm(mean(mag));
    mag_vec = [mag_vec(2), mag_vec(1), -mag_vec(3)];
    
    if(t1==t0)
        Down = -accel_vec;
        East = cross(Down, mag_vec)./norm(cross(Down, mag_vec));
        North = cross(East, Down)./norm(cross(East, Down));
        t1 = tic;
    else
        dt = toc(t1);

        teta = -mean(gyro).*dt;
        Down_gyro = RotateVector(Down, teta);
        East_gyro = RotateVector(East, teta);
        North_gyro = RotateVector(North, teta);

        Down_accel = -accel_vec;
        East_accel = cross(Down_accel, mag_vec)./norm(cross(Down_accel, mag_vec));
        North_accel = cross(East_accel, Down)./norm(cross(East_accel, Down));

        Down = Down_accel*weight + Down_gyro*(1-weight);
        East = East_accel*weight + East_gyro*(1-weight);
        North = North_accel*weight + North_gyro*(1-weight);
        t1 = tic;
    end
    if(norm(var(accel))<0.5)
        Down = -accel_vec;
        East = cross(Down, mag_vec)./norm(cross(Down, mag_vec));
        North = cross(East, Down)./norm(cross(East, Down));
    end

    North = North./norm(North);
    East = East./norm(East);
    Down = Down./norm(Down);

    C_head = [North', East', Down'];
    C_base = C_head.*0;

%     for i = 1:3
%         quiver3(C_base(1, i), C_base(2, i), C_base(3, i), C_head(1, i), C_head(2, i), C_head(3, i), 'Color', color(i), 'LineWidth', 2);
%         axis equal;
%         xlim([-1, 1]);
%         ylim([-1, 1]);
%         zlim([-1, 1]);
%         xlabel('x');
%         ylabel('y')
%         zlabel('z')
%         hold on;
%     end
%     hold off;

    free_accel = [free_accel; accel+g*Down];
    free_gyro = [free_gyro; gyro];
    hold off;
    for i=1:3
        subplot(3, 2, 2*i-1)
        plot(free_accel(:, i), "Color", color(i));
        if(length(free_accel)-500>0)
            xlim([length(free_accel)-500, length(free_accel)])
        end
        ylim([-20, 20]);
        title(acc_axes{i});
        hold on;
    end
    for i=1:3
        subplot(3, 2, 2*i)
        plot(free_gyro(:, i), "Color", color(i));
        if(length(free_gyro)-500>0)
            xlim([length(free_gyro)-500, length(free_gyro)])
        end
        ylim([-10, 10]);
        title(gyr_axes{i});
        hold on;
    end

%     hold off;
%     for i=1:3
%         subplot(3, 2, 2*i-1)
%         if(length(free_accel)-100>0)
%             plot(abs(fft(free_accel(end-100+1:end, i)))/100, "Color", color(i));
%         end
%         xlim([0, 100])
%         ylim([-2, 2]);
%         title(acc_axes{i});
%     end
%     for i=1:3
%         subplot(3, 2, 2*i)
%         if(length(free_gyro)-100>0)
%             plot(abs(fft(free_gyro(end-100+1:end, i)))/100, "Color", color(i));
%         end
%         xlim([0, 100])
%         ylim([-2, 2]);
%         title(gyr_axes{i});
%     end
    pause(0.01);

end 


