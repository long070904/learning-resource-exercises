%% IIR Filter Transient
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=4v1&lesson=5&section=3
% Requires NoisyFlute.wav (not bundled) and Signal Processing Toolbox.
% Standalone replay not independently executed.
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;

designedIIR = designfilt("bandpassiir", ...
    StopbandFrequency1=2100,PassbandFrequency1=2200, ...
    PassbandFrequency2=2500,StopbandFrequency2=2600, ...
    StopbandAttenuation1=60,PassbandRipple=1, ...
    StopbandAttenuation2=60,SampleRate=fs, ...
    DesignMethod="cheby1");
yiir = filter(designedIIR,marked);
%% Task 1 (Correct! 28 Sep 2026)
[hi,ti] = impz(designedIIR,2000,fs);
figure; plot(ti,hi)
%% Task 2 (Correct! 28 Sep 2026)
figure; plot(t,yiir)
%% Further Practice: section completed with one output, 28 Sep 2026
xlim([0 0.3])
soundsc(yiir,fs)
% Playback executed; no listening or subjective quality assessment claimed.
