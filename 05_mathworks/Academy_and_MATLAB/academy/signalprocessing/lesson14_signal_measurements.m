%% Signal Processing Onramp: verified measurement submissions
% Portal: https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=2&section=1
% The six tasks received "Correct!" in Academy. Tasks 4-5 were completed
% with a Live Editor task; see 14_signal_measurements_gui.md for settings.
% INPUT: the actual course wanc_bandpass must already be in the workspace.
% It is not bundled here. The plain-code equivalent below was checked against
% the actual live-task output with isequal in the hosted command window.

%% Task 1: calculate power over frequency and time
[p,f,t] = pspectrum(wanc_bandpass,50,"spectrogram");
% Observed sizes: p 1024x522, f 1024x1, t 522x1.

%% Task 2: aggregate across frequency bins
psum = sum(p);
plot(t,psum);

%% Task 3: express the aggregate power in decibels
pwr = db(psum,"power");
plot(t,pwr);

%% Tasks 4-5: verified plain-code equivalent of the Live Editor workflow
% Insert Find Local Extrema, input pwr, output maxIndices, X-axis t.
% Maxima; minimum prominence 10; minimum separation 0;
% maximum number 522; central selection for flat regions.
% This exact expression was verified with:
% assert(isequal(maxIndices,islocalmax(pwr,MinProminence=10)));
% The assertion returned without error using the real live-task maxIndices.
maxIndices = islocalmax(pwr,MinProminence=10);

%% Task 6: retain the corresponding time coordinates
quakeSec = t(maxIndices);
% Displayed event times, in seconds (rounded output):
% 115.33, 149.73, 184.13, 211.65, 235.73, 273.57, 388.81,
% 521.25, 572.85, 584.89, 624.45, 698.41, 713.89, 825.69.

%% Ungraded follow-up: mark event times on the filtered waveform
% This section ran successfully in Academy and created one output.
tvec = (0:numel(wanc_bandpass)-1)/50;
plot(tvec,wanc_bandpass);
xline(quakeSec);
xlabel("Time (seconds)");
