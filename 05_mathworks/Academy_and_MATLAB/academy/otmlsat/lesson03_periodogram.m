%% Spectral Analysis Techniques: verified periodogram tasks
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% All five tasks received "Correct!" in the hosted Academy runtime.
% INPUT: the course psdsig.mat is required and is not bundled here.
% Saved-script adaptation: separate figures retain the three displays.
% This .m display arrangement was not separately executed in Academy.

%% Course-provided startup
load psdsig;
sig=1e-3*sin(2*pi*fr*t);
n=length(sig);

%% Task 1: construct the window
w=ones(n,1);

%% Task 2: use the sample count for the transform length
nfft=n;

%% Task 3: plot with the specified window and transform length
figure('Name','Periodogram with specified parameters');
periodogram(sig,w,nfft,fs);

%% Task 4: use the default window and transform length
figure('Name','Periodogram with default parameters');
periodogram(sig,[],[],fs);

%% Task 5: retrieve and plot the numeric results
[p,f]=periodogram(sig,w,nfft,fs);
figure('Name','Periodogram numeric output');
plot(f,p);

% Conceptual follow-up guidelines were reviewed without an additional run.
