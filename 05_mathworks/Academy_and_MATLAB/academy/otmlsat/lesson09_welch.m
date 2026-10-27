%% Spectral Analysis Techniques: verified Welch tasks
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% All four tasks received "Correct!" in the hosted Academy runtime.
% INPUT: the course psdsig.mat is required and is not bundled here.
% Separate named figures are a saved-script display adaptation, not another
% verified execution. The accepted calculations are preserved.

%% Course-provided startup
load psdsig.mat;
whos;

%% Task 1: specify window and transform length
w=ones(n,1);
nfft=2^12;

%% Task 2: specify no overlap
numoverlap=0;

%% Task 3: calculate the spectrum with explicit parameters
figure('Name','Welch estimate with specified parameters');
pwelch(sig,w,numoverlap,nfft,fs);

%% Task 4: calculate the spectrum using defaults
figure('Name','Welch estimate with default parameters');
pwelch(sig,[],[],[],fs);

% The conceptual follow-up added no additional code or GUI activity.
