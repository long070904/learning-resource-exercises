%% Zero-Phase Filtering
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=4v1&lesson=4&section=2
% Academy flutefiltfilt.mlx; one task Correct! on 28 Sep 2026.
% Requires NoisyFlute.wav (not bundled) and Signal Processing Toolbox.
% Standalone figure arrangement not independently executed.
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;

designedIIR=designfilt('bandpassiir', ...
    'StopbandFrequency1',2100, ...
    'PassbandFrequency1',2200, ...
    'PassbandFrequency2',2500, ...
    'StopbandFrequency2',2600, ...
    'StopbandAttenuation1',60, ...
    'PassbandRipple',1, ...
    'StopbandAttenuation2',60, ...
    'SampleRate',fs);

figure; grpdelay(designedIIR,[],fs)
%% Accepted task
yiir = filtfilt(designedIIR,marked);
figure; plot(t,yin)
hold on
plot(t,yiir)
xlim([0.007 0.01])
hold off
legend(["original" "filtered"])
% Further Practice: forward/reverse filtering also works for linear-phase
% FIR filters, although a constant delay can instead be removed by shifting.
