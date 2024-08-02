%% Connection
clc, clear, close all;
if(exist('bt', 'var') == 0)
    bt = bluetooth('MPU9250'); 
end
disp('Connected.')

%% Calibration
calibrationTime = 2;
accel_list = [];
gyro_list = [];
t_list = [];
t0 = tic;
disp('Calibrating...');
while(toc(t0)<calibrationTime)
    data = fgetl(bt);
    value = cellfun(@str2double, split(data, ",")).';
    accel = value(1:3)/(16384);
    gyro = value(4:6)/(131*180/pi);
    t = value(7)/1000;
    
    accel_list = [accel_list; accel];
    gyro_list = [gyro_list; gyro];
    t_list = [t_list; t];
end
fs = length(t_list)/calibrationTime;
accel_var = var(accel_list);

gyro_var = var(gyro_list);
gyro_bias = mean(gyro_list);


gyro_list = gyro_list - gyro_bias;

disp('Calibration finished.');

%% Data Acquisition
accel_list = [];
gyro_list = [];
t_list = [];

flag_list = [];
accel_var_list =[];
gyro_var_list =[];

color = ['r', 'g', 'b'];
acc_axes = {'acc-x', 'acc-y', 'acc-z'};
gyr_axes = {'gyr-x', 'gyr-y', 'gyr-z'};

fopen(bt);
index=0;
window_size = floor(0.1*fs);
spr = 10;
threshold_rise = 5000;
threshold_fall = 800;
threshold = threshold_rise*[accel_var, gyro_var];


N_class = 4;
class_names = ['-', 'O', 'L', 'A'];
class_counter = 0;

X_train = cell(0);
y_train = [];

flushinput(bt);
t0 = tic;

while toc(t0)<120
    %
    for i=1:spr
        data = fgetl(bt);
        value = cellfun(@str2double, split(data, ",")).';
        accel = value(1:3)/(16384);
        gyro = value(4:6)/(131*180/pi) - gyro_bias;
        t = value(7)/1000;
        
        accel_list = [accel_list; accel];
        gyro_list = [gyro_list; gyro];
        t_list = [t_list; t];
        index=index+1;
    end
    %
    
    %
    if(length(t_list)>window_size)
        accel_var_list = [accel_var_list; var(accel_list(end-window_size+1:end, :))];
        gyro_var_list = [gyro_var_list; var(gyro_list(end-window_size+1:end, :))];
        disp(class_names(class_counter+1));
    
        if(any(var([accel_list(end-window_size+1:end, :), gyro_list(end-window_size+1:end, :)])>threshold))
            if(length(flag_list)>=2)
                if(flag_list(end)==0)
                    start_index = index + 1;
                end
            end
            flag_list = [flag_list, 1];
            threshold = threshold_fall*[accel_var, gyro_var];
        else
            if(length(flag_list)>=2)
                if(flag_list(end)==1)
                    X_train = [X_train; [accel_list(start_index:end, :), gyro_list(start_index:end, :), t_list(start_index:end, :)]];
                    y_train = [y_train, class_counter];
                    class_counter = mod(class_counter+1, N_class);
                end
            end
            flag_list = [flag_list, 0];
            threshold = threshold_rise*[accel_var, gyro_var];
        end
    end
    pause(0.0001);
    flushinput(bt);
end

%% Plotting
subplot(4, 1, 1);
plot([accel_var_list'; gyro_var_list'; flag_list]');
subplot(4, 1, 2);
plot([accel_list'; gyro_list']');
subplot(4, 1, 3);
s = X_train{1};
plot(s(:, 1:6));
subplot(4, 1, 4);
s = X_train{2};
plot(s(:, 1:6));

%% Saving
save('../../datasets/BBX/TrainSet.mat', 'X_train', 'y_train', 'class_names');