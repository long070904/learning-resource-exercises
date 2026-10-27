function spectral_analysis_methods()
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
if ~isfolder('results'), mkdir('results'); end
rng(42); fs=200; t=(0:1/fs:10-1/fs)';
x=sin(2*pi*12.3*t)+0.15*sin(2*pi*14*t)+0.3*randn(size(t));
N=numel(x); X=fft(x); amplitude=abs(X/N); amplitude=amplitude(1:N/2+1);
amplitude(2:end-1)=2*amplitude(2:end-1); frequencies=(0:N/2)'*fs/N;
[rect,f]=periodogram(x,rectwin(N),4096,fs);
[windowed,~]=periodogram(x,hann(N),4096,fs);
[welch,fw]=pwelch(x,hann(400),200,4096,fs);
[welchShort,fsw]=pwelch(x,hann(100),75,4096,fs);
figure; tiledlayout(2,1);
nexttile; plot(f,10*log10(rect+eps),f,10*log10(windowed+eps));
xlim([8 20]); legend('Rectangular','Hann'); ylabel('PSD (dB/Hz)');
nexttile; plot(fw,10*log10(welch+eps),fsw,10*log10(welchShort+eps));
xlim([8 20]); legend('400-sample windows','100-sample windows'); xlabel('Hz');
exportgraphics(gcf,'results/spectral_methods.png');
% Parametric and subspace techniques on a short signal. AR order is a modelling choice.
short=x(1:160);
[burg,fb]=pburg(short,12,4096,fs);
[music,fm]=pmusic(short,4,4096,fs); % two real sinusoids span four complex components
figure; tiledlayout(2,1);
nexttile; plot(fb,10*log10(burg+eps)); xlim([0 40]); title('Burg AR PSD');
nexttile; plot(fm,10*log10(music+eps)); xlim([0 40]); title('MUSIC pseudospectrum');
exportgraphics(gcf,'results/parametric_spectrum.png');
save('results/spectrum_arrays.mat','amplitude','frequencies','rect','windowed','welch','burg','music');
disp('Zero padding samples the same spectrum more densely; it does not increase physical resolving power.');
disp('MUSIC is a pseudospectrum and its magnitude is not a calibrated PSD.');
end
