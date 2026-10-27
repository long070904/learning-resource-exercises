%% Time-Frequency Analysis: effect of window length on a spectrogram
% Source: https://matlabacademy.mathworks.com/details/time-frequency-analysis/otmltfa
% In the ungraded spectropara.mlx GUI activity, the window-length control
% was changed from 260 to 500. Academy reported a completed run with one
% output; the displayed 25 Hz and 26 Hz bands were separated.
% This counts as one GUI activity, not another code example or graded task.
% This saved script fixes the verified control value; its standalone replay
% has not been independently executed.

fs=100;
t=(0:1/fs:10)';
y1=sin(2*pi*25*t);
y2=sin(2*pi*26*t);
y=y1+y2;
w=hamming(500);
spectrogram(y,w,[],[],fs);
