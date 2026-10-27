function onramp_signal_workflow()
% Onramp topics: import, time base, region, alignment, PSD, filters, measurements.
% Source: https://matlabacademy.mathworks.com/details/signal-processing-onramp/signalprocessing
if ~isfolder('results'), mkdir('results'); end
T = readtable('data/synthetic_signal.csv');
t = T.time_seconds; x = T.raw; fs = 1/median(diff(t));
assert(all(diff(t)>0));
TT = timetable(seconds(t),x,'VariableNames',{'Signal'});
disp(TT(1:5,:));
% Signal Analyzer GUI task: run signalAnalyzer(x,'SampleRate',fs) interactively.
% The remaining functions are a reproducible script equivalent of core operations.
region = t>=2 & t<6;
xRegion = x(region); tRegion = t(region);
xDetrended = detrend(xRegion);
[b,a] = butter(4,20/(fs/2),'low');
xFiltered = filtfilt(b,a,xDetrended); % offline, forward/backward filtering
[psd,f] = pwelch(xFiltered,hann(200),100,1024,fs);
figure; tiledlayout(2,1);
nexttile; plot(tRegion,xRegion,tRegion,xFiltered); xlabel('Time (s)');
ylabel('Amplitude'); legend('Raw','Filtered');
nexttile; plot(f,10*log10(psd+eps)); xlim([0 80]);
xlabel('Frequency (Hz)'); ylabel('PSD (amplitude^2/Hz, dB)');
exportgraphics(gcf,'results/onramp_signal.png');
[peaks,locations] = findpeaks(xFiltered,fs,'MinPeakDistance',0.15,'MinPeakProminence',0.5);
measurements = table(rms(xFiltered),peak2peak(xFiltered),numel(peaks), ...
    'VariableNames',{'RMS','PeakToPeak','PeakCount'});
disp(measurements); writetable(measurements,'results/onramp_measurements.csv');
save('results/onramp_arrays.mat','tRegion','xRegion','xFiltered','psd','f','locations');
end
