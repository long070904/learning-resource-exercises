%% Signal Processing Onramp: ungraded steepness comparison
% Portal: https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=5v1&lesson=2&section=1
% Requires the course's wanc array already loaded into the workspace.
% These commands completed without error in the hosted command window.
% Both outputs were 45107-by-1 and a Figure 1 tab was created. The graphic
% was obscured by Signal Analyzer, so its curves were not visually checked.

soft = lowpass(wanc,0.1,50,Steepness=0.5);
sharp = lowpass(wanc,0.1,50,Steepness=0.99);
figure;
plot([soft sharp]);
legend("0.5","0.99");
