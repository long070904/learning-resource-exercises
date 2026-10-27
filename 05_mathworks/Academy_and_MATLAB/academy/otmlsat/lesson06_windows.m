%% Spectral Analysis Techniques: replay of verified window settings
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% All five Academy tasks passed, using Window Designer for Tasks 1 and 3-5.
% See lesson06_windows_gui.md for the actual graded GUI actions.
% INPUT: the course psdsig.mat is required and is not bundled here.
% ADAPTATION: ones/hamming/kaiser replay the selected window settings without
% the GUI, and named figures retain the plots. This standalone replay was
% not executed or compared numerically against the exported GUI windows.

%% Course-provided startup
load psdsig;
sig=1e-3*sin(2*pi*fr*t);
n=length(sig);

%% Task 1 setting: rectangular window, length 2400 in the course
% Academy created w through Window Designer and saved it to the workspace.
w=ones(n,1);
figure('Name','Rectangular window');
plot(t,w);

%% Task 2: accepted periodogram computation
figure('Name','Rectangular-window periodogram');
periodogram(sig,w,2^12,fs);

%% Task 3 setting: Hamming window, length 2400
w=hamming(n);
figure('Name','Hamming-window periodogram');
periodogram(sig,w,2^12,fs);

%% Task 4 setting: Kaiser window, length 2400, beta 1
w=kaiser(n,1);
figure('Name','Kaiser beta 1 periodogram');
periodogram(sig,w,2^12,fs);

%% Task 5 setting: Kaiser window, length 2400, beta 20
w=kaiser(n,20);
figure('Name','Kaiser beta 20 periodogram');
periodogram(sig,w,2^12,fs);
