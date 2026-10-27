%% Filter Design and Analysis Methods: design with Filter Designer
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=3v1&lesson=2&section=2
% One ungraded GUI workflow was completed on 25 Sep 2026; it is not a
% graded task or an additional ungraded code example.
% INPUT: the course NoisyFlute.wav is required and is not bundled.
% TOOLBOX: Signal Processing Toolbox.
% Filter Designer exported bandpassfir1_Num as a 1x201 double. In Academy,
% bReplay=fir1(200,[2200 2500]/(fs/2),rectwin(201)); followed by
% max(abs(bReplay-bandpassfir1_Num)) returned 0. The reconstruction below
% therefore matches the observed export exactly for this course run.
% Separate named figures retain displays; this complete standalone replay
% was not independently executed.

%% Course signal setup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;
figure('Name','Watermarked flute and target band');
pwelch(marked,[],[],[],fs);
xline(2200/1000,"m--");
xline(2500/1000,"m--");

%% Equivalent reconstruction of the verified GUI coefficient export
% Bandpass FIR, Window method, Rectangular window, sample rate 16000 Hz,
% order 200, and 6 dB cutoff frequencies 2200 Hz and 2500 Hz.
bandpassfir1_Num=fir1(200,[2200 2500]/(fs/2),rectwin(201));

%% Filtering performed as part of the same GUI workflow
yout=filter(bandpassfir1_Num,1,marked);
figure('Name','Filter Designer coefficient output spectrum');
pwelch(yout,[],[],[],fs);
