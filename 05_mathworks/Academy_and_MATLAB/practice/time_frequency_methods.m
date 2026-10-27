function time_frequency_methods()
% Source: https://matlabacademy.mathworks.com/details/time-frequency-analysis/otmltfa
if ~isfolder('results'), mkdir('results'); end
rng(42); fs=200; t=(0:1/fs:10-1/fs)';
x=chirp(t,5,t(end),65)+0.1*randn(size(t));
% A synthetic fan-like transient is a topic demonstration, not the supplied Academy project.
fault=2*sin(2*pi*75*t).*(t>=4 & t<4.25); x=x+fault;
figure; tiledlayout(2,1);
nexttile; spectrogram(x,hann(128),112,512,fs,'yaxis'); title('Longer window');
nexttile; spectrogram(x,hann(32),24,512,fs,'yaxis'); title('Shorter window');
exportgraphics(gcf,'results/spectrogram_comparison.png');
% Wavelet Toolbox is required for the scalogram branch.
if exist('cwt','file')==2
    figure; cwt(x,fs,'VoicesPerOctave',12); title('Wavelet scalogram: 12 voices/octave');
    exportgraphics(gcf,'results/scalogram_12.png');
    figure; cwt(x,fs,'VoicesPerOctave',24); title('Wavelet scalogram: 24 voices/octave');
    exportgraphics(gcf,'results/scalogram_24.png');
else
    warning('Wavelet Toolbox unavailable: scalogram examples were not run.');
end
save('results/time_frequency_arrays.mat','t','x','fault');
disp('Shorter STFT windows improve time localisation but broaden frequency peaks.');
end
