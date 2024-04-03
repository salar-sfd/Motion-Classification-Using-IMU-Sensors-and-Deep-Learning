% Create a Bluetooth object
bt = bluetooth('HC-05', 1); % Replace 'HC-05' with the correct device name

% Open the Bluetooth connection
fopen(bt);

% Read and process IMU data
while true
    % Read a line of data from the Bluetooth connection
    data = fgetl(bt);
    
    % Split the data into individual values
    values = split(data, ",");
    
    % Convert the values to numeric format
    accX = str2double(values(1));
    accY = str2double(values(2));
    accZ = str2double(values(3));
    gyroX = str2double(values(4));
    gyroY = str2double(values(5));
    gyroZ = str2double(values(6));
    magX = str2double(values(7));
    magY = str2double(values(8));
    magZ = str2double(values(9));
    
    % Process the IMU data as desired
    % ...
end

% Close the Bluetooth connection
fclose(bt);