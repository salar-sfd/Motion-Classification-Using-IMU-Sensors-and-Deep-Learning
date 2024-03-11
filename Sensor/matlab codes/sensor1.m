clc, clear, close all;

a = arduino('COM13', 'Uno');

fs = 100;
imu = mpu9250(a, 'SampleRate', fs, 'OutputFormat', 'matrix');
color = ['r', 'g', 'b'];
ts = tic; 
stopTimer = 10; 
figure;
    points = [];

while(toc(ts) < stopTimer) 
    [accel, gyro, mag] = read(imu);
    accel_vec = mean(accel)./norm(mean(accel));
%     gyro_vec = mean(gyro)./norm(mean(gyro));
    mag_vec = mean(mag)./norm(mean(mag));
    
    Down = -accel_vec;
    East = cross(Down, mag_vec)./norm(cross(Down, mag_vec));
    North = cross(East, Down)./norm(cross(East, Down));

    C_head = [North', East', Down'];
    C_base = C_head.*0;
    for i = 1:3
        quiver3(C_base(i, 1), C_base(i, 2), C_base(i, 3), C_head(i, 1), C_head(i, 2), C_head(i, 3), 'Color', color(i), 'LineWidth', 2);
        axis equal;
        xlim([-1, 1]);
        ylim([-1, 1]);
        zlim([-1, 1]);
        xlabel('x');
        ylabel('y')
        zlabel('z')
        hold on;
    end
    disp(accel_vec)

    points = [points; North];
    pause(0.01);
    hold off;

end 
figure
scatter3(points(:, 1), points(:, 2), points(:, 3), 'filled');
axis equal;
xlabel('X');
ylabel('Y');
zlabel('Z');
xlim([-1, 1]);
ylim([-1, 1]);
zlim([-1, 1]);
title('Scatter 3D Plot');