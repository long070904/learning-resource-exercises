function signal_generation_resampling()
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Synthetic tones, chirp, square wave, watermark; not the Academy's hidden assets.
if ~isfolder('results'), mkdir('results'); end
fs=200; t=(0:1/fs:5-1/fs)';
tone=sin(2*pi*8*t); sweeping=chirp(t,5,t(end),70);
squareWave=square(2*pi*5*t); watermark=0.05*sin(2*pi*35*t);
combined=tone+watermark;
% Rational conversion includes an anti-aliasing filter, unlike bare indexing.
newFs=80; [p,q]=rat(newFs/fs);
resampled=resample(combined,p,q);
squareResampled=resample(squareWave,p,q);
upsampled=upsample(tone,2); reconstructed=resample(tone,2,1);
% Demonstrate aliasing of a 70 Hz tone sampled at 80 Hz: it appears at 10 Hz.
original70=sin(2*pi*70*t); newT=(0:1/newFs:5-1/newFs)';
aliased70=sin(2*pi*70*newT);
[P,F]=periodogram(aliased70,[],4096,newFs); [~,idx]=max(P);
assert(abs(F(idx)-10)<0.1);
figure; tiledlayout(3,1);
nexttile; plot(t,combined); xlim([0 1]); title('Tone plus synthetic watermark');
nexttile; plot((0:numel(resampled)-1)/newFs,resampled); xlim([0 1]); title('Rational resampling');
nexttile; plot(F,10*log10(P+eps)); title('Aliasing demonstration'); xlabel('Hz');
exportgraphics(gcf,'results/resampling.png');
% Audio upsampling practice uses an original generated tone.
audioFs=8000; audioTime=(0:audioFs-1)'/audioFs;
audio=0.3*sin(2*pi*440*audioTime); audioUp=resample(audio,2,1);
audiowrite('results/original_tone.wav',audio,audioFs);
audiowrite('results/upsampled_tone.wav',audioUp,2*audioFs);
save('results/resampling_arrays.mat','sweeping','squareWave','squareResampled', ...
    'watermark','resampled','upsampled','reconstructed','original70','aliased70');
disp('Square-wave harmonics above the new Nyquist frequency are removed before downsampling.');
end
