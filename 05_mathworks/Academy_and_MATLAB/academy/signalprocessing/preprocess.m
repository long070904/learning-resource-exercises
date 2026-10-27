function y = preprocess(x,tx)
% Course-provided generated function, preserved from Signal Processing Onramp.
% https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=1&section=1
% Export provenance: MATLAB 9.14, Signal Processing Toolbox 9.2,
% 23 March 2023. Used successfully on the course HARP recording.
Fs = 1/mean(diff(tx));
y = bandpass(x,[2 10],Fs,'Steepness',0.85,'StopbandAttenuation',60);
