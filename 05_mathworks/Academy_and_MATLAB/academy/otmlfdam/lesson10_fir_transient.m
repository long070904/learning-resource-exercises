%% FIR Filter Transient
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=4v1&lesson=5&section=2
% Academy flutetransientfir.mlx.
% Requires NoisyFlute.wav (not bundled) and Signal Processing Toolbox.
% Standalone figures have not been independently executed.
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
%% Task 1: filter order (Correct! 28 Sep 2026)
o = filtord(designedFIR);
%% Task 2: impulse response (Correct! 28 Sep 2026)
[hi,ti] = impz(designedFIR,500,fs);
figure; plot(ti,hi)
%% Task 3: end of transient (Correct! 28 Sep 2026)
tc = t(o);
%% Task 4: mark transient boundary (Correct! 28 Sep 2026)
figure; plot(t,yfir)
xline(tc)
%% Further Practice: verified run with two outputs, 28 Sep 2026
xlim([0 0.1])
figure
plot(t(o:end),yfir(o:end))
