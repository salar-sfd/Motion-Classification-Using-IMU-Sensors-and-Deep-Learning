clc, clear, close all;

a = arduino('COM13', 'Uno');

fs = 200;
weight = 0.0;
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix', 'SamplesPerRead', 10);


t0 = tic;
calibrationTimer = 2;
g_list = [];
while(toc(t0)<calibrationTimer)
    [accel, ~, ~] = read(imu);
    g_list = [g_list; vecnorm(accel, 2, 2)];
end
g = mean(g_list);
x = [0, 0];
v = [0, 0];
%% 


color = ['r', 'g', 'b'];
t0 = tic;
t1 = t0;
tx = tic;
stopTimer = 400;
accel_hist = [];
figure;

p = [];
points = [];
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

    p = [p; accel+g*Down];

    North = North./norm(North);
    East = East./norm(East);
    Down = Down./norm(Down);
    points = [points; North];

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
    pause(0.01);
%     hold off;
%     for i=1:3
%         subplot(3, 1, i)
%         plot(p(:, i), "Color", color(i));
%         if(length(p)-500>0)
%             xlim([length(p)-500, length(p)])
%         end
%         ylim([-30, 20]);
%         hold on;
%     end
    dt = toc(tx);
    tx = tic;
    v = v + p(end, [1,3])*dt;
    v = v*exp(0);
    x = x + v*dt;

    if(x(1)>1)
        v=v*0;
        x(1)=1; end
    if(x(1)<-1)
        v=v*0;
        x(1)=-1; end
    if(x(2)>1)
        v=v*0;
        x(2)=1; end
    if(x(2)<-1)
        v=v*0;
        x(2)=-1; end


    scatter(x(1)*5, x(2)*5);
    xlim([-5, 5])
    ylim([-5, 5])
    hold on;

end 
% scatter3(points(:, 1), points(:, 2), points(:, 3), 'filled');
% axis equal;
% xlabel('X');
% ylabel('Y');
% zlabel('Z');
% xlim([-1, 1]);
% ylim([-1, 1]);
% zlim([-1, 1]);
% title('Scatter 3D Plot');
% 
% figure;
