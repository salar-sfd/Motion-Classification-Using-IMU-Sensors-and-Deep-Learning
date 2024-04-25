clc, clear, close all;

%% Loading
load('../../datasets/BBX/TrainSet.mat');

x_train = cell(0);

for i = 1:numel(X_train)
    x = X_train{i};
    x_train = [x_train; x(:, 1:6)'];
end

N_train = numel(x_train);
for i=1:N_train
    x = x_train{i};
    T_train(i) = size(x,2);
end
[T_train,indices] = sort(T_train);
x_train = x_train(indices);
y_train = y_train(indices);

figure
bar(T_train)
xlabel("Sequence")
ylabel("Length")
title("Sorted Data")
%% Network
Nf = 6;

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
    fullyConnectedLayer(4)
    softmaxLayer
    classificationLayer];

%% Training
maxEpochs = 20;
miniBatchSize = 1;

options = trainingOptions('adam', ...
    'ExecutionEnvironment','cpu', ...
    'GradientThreshold',1, ...
    'MaxEpochs',maxEpochs, ...
    'MiniBatchSize',miniBatchSize, ...
    'SequenceLength','longest', ...
    'Shuffle','never', ...
    'Verbose',0, ...
    'Plots','training-progress');

y_train_categorical = categorical(y_train');
net = trainNetwork(x_train, y_train_categorical, layers, options);

%%
y_train_pred = classify(net, x_train);

confusion = confusionmat(y_train_categorical, y_train_pred);

%%
save('../../datasets/BBX/net.mat', 'net', 'class_names');