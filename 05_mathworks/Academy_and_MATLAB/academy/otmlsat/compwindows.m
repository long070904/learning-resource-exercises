%% Spectral Analysis Techniques: course-provided window comparison
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% The original compwindows.mlx completed in Academy with two outputs.
% ADAPTATION: separate named figures retain its two sections outside the
% Live Editor. This saved .m arrangement was not separately executed.
% The supplied 10*log10(abs(h)) expression and Power (dB) label are preserved.
% They are not presented here as a calibrated power spectral density.

fs=50;
n=50;
wrect=ones(n,1);
wham=hamming(n);
wk1=kaiser(n,1);
wk6=kaiser(n,6);
wk20=kaiser(n,20);

%% Compare three window types
figure('Name','Rectangular, Hamming, and Kaiser windows');
winfreq(wrect,fs);
hold on;
winfreq(wham,fs);
winfreq(wk1,fs);
hold off;
legend("Rectangular","Hamming","Kaiser Beta 1");

%% Compare Kaiser beta values
figure('Name','Kaiser beta comparison');
winfreq(wk1,fs);
hold on;
winfreq(wk6,fs);
winfreq(wk20,fs);
hold off;
legend("Beta 1","Beta 6","Beta 20");

function winfreq(win,fs)
    [h,f]=freqz(win,1,2^17,fs);
    plot(f,10*log10(abs(h)),"LineWidth",2);
    xlabel("Frequency (Hz)");
    ylabel("Power (dB)");
end
