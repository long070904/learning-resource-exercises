%% Compensate for Group Delay
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=4v1&lesson=4&section=1
% Academy source: flutecompdelay.mlx
% Requires course NoisyFlute.wav (not bundled) and Signal Processing Toolbox.
% This standalone replay has not been independently executed.

%% Provided setup
[flute,fs] = audioread("NoisyFlute.wav");
flute = flute(1:3*fs);
t = ((0:numel(flute)-1)/fs)';
yin = chirp(t,2200,t(end),2500)*0.0005;
marked = flute + yin;
designedFIR = designfilt("bandpassfir", ...
    StopbandFrequency1=2100,PassbandFrequency1=2200, ...
    PassbandFrequency2=2500,StopbandFrequency2=2600, ...
    StopbandAttenuation1=80,PassbandRipple=1, ...
    StopbandAttenuation2=60,SampleRate=fs);
yfir = filter(designedFIR,marked);
figure; grpdelay(designedFIR,[],fs)
figure; plot(t,yin)
hold on
plot(t,yfir)
xlim([0.007 0.01])
hold off
legend(["original" "filtered"])

%% Task 1: determine the constant delay (Correct! observed 25 Sep 2026)
gd = grpdelay(designedFIR);
delay = gd(1);

%% Task 2: remove the delayed samples (Correct! observed 28 Sep 2026)
yfir(1:delay) = [];

%% Task 3: match the shifted signal length (Correct! observed 28 Sep 2026)
tadj = t(1:end-delay);

%% Task 4: compare aligned signals (Correct! observed 28 Sep 2026)
figure; % Separate figure for this standalone replay.
plot(t,yin)
hold on
plot(tadj,yfir)
xlim([0.007 0.01])
hold off
legend(["original" "filtered"])
% Further Practice was conceptual: a constant delay allows this alignment;
% a nonlinear-phase filter delays different frequencies by different amounts.
