% Course-provided generated script, preserved from Signal Processing Onramp.
% https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=1&section=1
% Export provenance: MATLAB 9.14, Signal Processing Toolbox 9.2,
% 23 March 2023. Requires the course wanc_bandpass workspace variable.
% This script executed successfully in the hosted command window.
timeLimits = [0 902.12];
frequencyLimits = [0 25];
overlapPercent = 50;
wanc_bandpass_ROI = wanc_bandpass(:);
sampleRate = 50;
startTime = 0;
timeValues = startTime+(0:length(wanc_bandpass_ROI)-1).'/sampleRate;
minIdx = timeValues>=timeLimits(1);
maxIdx = timeValues<=timeLimits(2);
wanc_bandpass_ROI = wanc_bandpass_ROI(minIdx&maxIdx);
timeValues = timeValues(minIdx&maxIdx);
[P,F,T] = pspectrum(wanc_bandpass_ROI,timeValues,'spectrogram', ...
    'FrequencyLimits',frequencyLimits,'OverlapPercent',overlapPercent);
