function filter_design_analysis()
% Source: https://matlabacademy.mathworks.com/details/filter-design-and-analysis-methods/otmlfdam
if ~isfolder('results'), mkdir('results'); end
T=readtable('data/synthetic_signal.csv'); x=T.raw; reference=T.clean_reference; fs=200;
fir=fir1(100,20/(fs/2),'low',hamming(101));
[b,a]=butter(6,20/(fs/2),'low');
specFilter=designfilt('lowpassiir','PassbandFrequency',15,'StopbandFrequency',40, ...
    'PassbandRipple',1,'StopbandAttenuation',50,'SampleRate',fs);
offline=filtfilt(b,a,x); causal=filter(b,a,x);
[bp,ap]=butter(4,[4 16]/(fs/2),'bandpass'); band=filter(bp,ap,x);
[H,F]=freqz(b,a,2048,fs); [delay,fd]=grpdelay(b,a,2048,fs);
assert(all(abs(roots(a))<1));
figure; tiledlayout(2,2);
nexttile; plot(F,20*log10(abs(H)+eps)); xlabel('Hz'); ylabel('Magnitude (dB)');
nexttile; plot(fd,delay); xlim([0 30]); ylabel('Group delay (samples)'); xlabel('Hz');
nexttile; impz(b,a); title('Impulse response');
nexttile; zplane(b,a); title('Stable IIR poles');
exportgraphics(gcf,'results/filter_analysis.png');
% Arbitrary magnitude response practice (normalised 0..1 Nyquist frequency).
custom=fir2(100,[0 .1 .3 .5 .7 1],[1 1 .5 .5 .1 0]);
figure; freqz(custom,1,1024,fs); exportgraphics(gcf,'results/arbitrary_filter.png');
% Synthetic watermark verification through a narrow bandpass.
t=T.time_seconds; watermark=0.05*sin(2*pi*35*t); composite=reference+watermark;
[wmB,wmA]=butter(4,[32 38]/(fs/2),'bandpass'); recovered=filtfilt(wmB,wmA,composite);
measurements=table(rms(x-reference),rms(offline-reference),max(abs(roots(a))), ...
    'VariableNames',{'RawErrorRMS','OfflineErrorRMS','LargestPoleMagnitude'});
disp(measurements);writetable(measurements,'results/filter_measurements.csv');
save('results/filter_arrays.mat','fir','b','a','offline','causal','band','custom','recovered','specFilter');
disp('Inspect edge transients. Zero-phase filtfilt is an offline method and uses future samples.');
% GUI practice, when working interactively: filterDesigner
end
