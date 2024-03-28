%%
clc, clear, close all;

%% Train Preprocessing
load('../datasets/train2.mat');

mu_y = mean(y);
std_y = std(y);
y = (y - mu_y)./std_y;

window_size = 64;
window_step = 1;
Nf = size(x, 2);
x_train = cell(floor((size(x, 1)-window_size+1)/window_step), 1);
y_train = zeros(floor((size(x, 1)-window_size+1)/window_step), 2);

for i = 0:size(x_train, 1)-1
    x_train{i+1} = x(i*window_step+1:i*window_step+window_size, :)';
    y_train(i+1, :) = y(i*window_step+1, :);
end

%% Eval Preprocessing
load('../datasets/eval2.mat');

y = (y - mu_y)./std_y;

window_size = 64;
window_step = 1;
Nf = size(x, 2);
x_eval = cell(floor((size(x, 1)-window_size+1)/window_step), 1);
y_eval = zeros(floor((size(x, 1)-window_size+1)/window_step), 2);

for i = 0:size(x_eval, 1)-1
    x_eval{i+1} = x(i*window_step+1:i*window_step+window_size, :)';
    y_eval(i+1, :) = y(i*window_step+1, :);
end
%% Network

numResponses = 2;

layers = [
    sequenceInputLayer(Nf)
    convolution1dLayer(3, 64, Padding="causal")
    reluLayer
    layerNormalizationLayer
    convolution1dLayer(3 , 32, Padding="causal")
    reluLayer
    layerNormalizationLayer
    convolution1dLayer(3 , 16, Padding="causal")
    reluLayer
    layerNormalizationLayer
    globalAveragePooling1dLayer
    fullyConnectedLayer(16)
    fullyConnectedLayer(16)
    fullyConnectedLayer(2)
    regressionLayer];

%% Training
options = trainingOptions("adam", ...
    MiniBatchSize = 128, ...
    MaxEpochs = 24, ...
    ValidationData = {x_eval y_eval}, ...
    OutputNetwork = "best-validation-loss", ...
    InitialLearnRate = 0.005, ...
    Plots = "training-progress", ...
    Verbose = false);

net = trainNetwork(x_train, y_train, layers, options);

%% Testing
y_train_pred = predict(net,x_train, SequenceLength="shortest");
y_eval_pred = predict(net,x_eval, SequenceLength="shortest");

%% Plotting
index = 1500:2000;
subplot(2, 2, 1)
plot(y_eval(index, 1))
hold on
plot(y_eval_pred(index, 1))
title('Eval')
subplot(2, 2, 3)
plot(y_eval(index, 2))
hold on
plot(y_eval_pred(index, 2))
subplot(2, 2, 2)
plot(y_train(index, 1))
hold on
plot(y_train_pred(index, 1))
title('Train')
subplot(2, 2, 4)
plot(y_train(index, 2))
hold on
plot(y_train_pred(index, 2))