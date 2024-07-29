%% Loading Training Dataset
clc, clear, close all;
load('train_set.mat');

%% Preprocessing
mu = mean(x, 1);
std = std(x, 0, 1);
x = (x-mu)./std;

window_size = 20;
window_step = 2;
Nf = size(x, 2);
x_train = cell(floor((size(x, 1)-window_size+1)/window_step), 1);
y_train = zeros(floor((size(x, 1)-window_size+1)/window_step), 2);

% x_train = zeros(floor((size(x, 1)-window_size+1)/window_step), window_size, Nf);
% y_train = zeros(floor((size(y, 1)-window_size+1)/window_step), 2);
for i = 0:size(x_train, 1)-1
    x_train{i+1} = x(i*window_step+1:i*window_step+window_size, :)';
    y_train(i+1, :) = y(i*window_step+1, :);
end

% x_train = mat2cell(x_train, ones(size(x_train, 1), 1), size(x_train, 2), size(x_train, 3));
% y_train = mat2cell(y_train, ones(size(y_train, 1), 1), size(y_train, 2));

%% Defining Network
% layers = [
%     sequenceInputLayer(Nf)
% %     convolution1dLayer(3,30,Padding="causal")
%     reluLayer
% %     convolution1dLayer(3, 5, 'Padding', 'same')
%     reluLayer
% %     maxPooling1dLayer(2)
% %     convolution1dLayer(3, 10, 'Padding', 'same')
%     reluLayer
% %     convolution1dLayer(3, 10, 'Padding', 'same')
%     reluLayer
% %     maxPooling1dLayer(2)
%     flattenLayer
%     fullyConnectedLayer(20)
%     reluLayer
%     fullyConnectedLayer(20)
%     reluLayer
%     fullyConnectedLayer(1) % Single output neuron for regression
%     regressionLayer()
%     ];

layers = [ ...
    sequenceInputLayer(Nf)
    lstmLayer(window_size, OutputMode="last")
    fullyConnectedLayer(window_size)
    reluLayer
    fullyConnectedLayer(window_size)
    reluLayer
    fullyConnectedLayer(2)
    regressionLayer];

lossFunction = 'mse';

options = trainingOptions("adam", ...
    MaxEpochs=15, ...
    SequencePaddingDirection="left", ...
    Plots="training-progress", ...
    Verbose=0);

% Train the network
trainedNet = trainNetwork(x_train, y_train, layers, options);