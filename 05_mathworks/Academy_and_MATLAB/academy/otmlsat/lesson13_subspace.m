%% Spectral Analysis Techniques: subspace methods
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% The graded task received "Correct!" on 25 Sep 2026 with 0.5 seconds
% (501 samples) and numtones=6. The optional GUI practice changed numtones
% to 10, showed spurious peaks, and restored 6. The Try MUSIC code example
% was then run separately; Academy reported a completed section with
% three outputs. These are one GUI activity and one code comparison.
% Separate named figures below retain each display in a plain .m file;
% this standalone arrangement was not independently executed.

%% Verified duration and course signal
fs=1000;
t=(0:1/fs:0.5)';
disp(numel(t)+" samples");
x=sin(2*pi*220*t)+sin(2*pi*200*t)+0.1*sin(2*pi*100*t);
rng default;
xn=x+0.1*randn(size(x));
numtones=6;

%% Course eigenvector estimate
figure('Name','Eigenvector estimate with six components');
peig(xn,numtones,2^10,fs);

%% Verified Try MUSIC comparison (uncommented in Academy)
figure('Name','MUSIC estimate with six components');
pmusic(xn,numtones,2^10,fs);

%% Course Welch and periodogram comparisons
figure('Name','Welch estimate of the short signal');
pwelch(xn,[],[],2^10,fs);
figure('Name','Periodogram of the short signal');
periodogram(xn,[],2^10,fs);

%% Replay of the optional GUI experiment with excessive components
% The Academy numtones control was changed to 10 and then restored to 6.
% This explicit replay preserves that experiment outside the GUI.
figure('Name','Eigenvector estimate with ten components');
peig(xn,10,2^10,fs);
