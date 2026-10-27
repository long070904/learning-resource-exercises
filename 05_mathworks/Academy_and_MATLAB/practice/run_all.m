function run_all()
% Original worked practice mapped to public MathWorks course topics.
% These files are not extracted Academy task answers or completion evidence.
% Requires MATLAB and Signal Processing Toolbox. Wavelets are optional.
original = pwd; cleanup = onCleanup(@() cd(original));
cd(fileparts(mfilename('fullpath')));
if ~isfolder('results'), mkdir('results'); end
onramp_signal_workflow();
signal_generation_resampling();
spectral_analysis_methods();
time_frequency_methods();
filter_design_analysis();
wearable_preprocessing();
disp('Local practice scripts finished. Review results and any toolbox notices.');
end
