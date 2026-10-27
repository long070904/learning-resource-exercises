%% Arbitrary Filter Response
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=5v1&lesson=2&section=3
% Requires course whalesound.wav, simplified absorption.m, and Signal
% Processing Toolbox. Course assets are not bundled.
% Standalone replay not independently executed.
[whaley,fs] = audioread("whalesound.wav");
n = numel(whaley);
fr = (0:n-1)*(fs/n);
fr = fr(1:n/2+1);
waterabs = absorption(fr);
fabs = fr/fs*2;

%% Task 1 (Correct! observed 28 Sep 2026)
b = fir2(10,fabs,waterabs);
a = 1;

%% Task 2 (Correct! observed 28 Sep 2026)
whalefilt = filter(b,a,whaley);

%% Task 3 (Correct! observed 28 Sep 2026)
[h,f] = freqz(b,a,512,fs);

%% Task 4 (Correct! observed 28 Sep 2026)
figure; % Separate figure in standalone replay.
plot(fr,waterabs)
hold on
plot(f,abs(h))
hold off

%% Task 5 (Correct! observed 28 Sep 2026)
% Academy changed the earlier design line and reran the script.
% Replay explicitly repeats dependent calculations for the new design.
b = fir2(30,fabs,waterabs);
a = 1;
whalefilt = filter(b,a,whaley);
[h,f] = freqz(b,a,512,fs);
figure; plot(fr,waterabs)
hold on; plot(f,abs(h)); hold off
%% Task 6 (Correct! observed 28 Sep 2026)
% Academy replaced the earlier FIR design and removed a=1.
[b,a] = yulewalk(10,fabs,waterabs);
whalefilt = filter(b,a,whaley);
[h,f] = freqz(b,a,512,fs);
figure; plot(fr,waterabs)
hold on; plot(f,abs(h)); hold off
%% Suggested playback (completed with no outputs, 28 Sep 2026)
sound(whaley,fs)
pause(numel(whaley)/fs+0.5)
sound(whalefilt,fs)
% Playback execution verified; no listening or quality assessment claimed.
