%% Signal Processing Onramp: verified ungraded generated-code examples
% Portal: https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=1&section=1
% Both examples below executed in the hosted MATLAB command window and
% returned to the prompt without errors. This lesson did not assign grades.
% Required input: the real course after_filtering.mat, which is not bundled.
% Keep the saved preprocess.m and wanc_spect.m on the MATLAB path.

%% Course-provided startup data and time grid
load("after_filtering.mat");
t = (0:numel(harp)-1)/50;
% The course startup also opened preprocess.m and wanc_spect.m for review.
% The two helper files are preserved alongside this driver.

%% Ungraded example 1: run the provided spectrum script
wanc_spect;

%% Ungraded example 2: apply the provided function to HARP
h = preprocess(harp,t);
figure;
plot(t,h);
% The rendered HARP plot was visually checked in Academy: amplitude was
% about 1e-3, with visible edge artifacts. No course grade is claimed.
