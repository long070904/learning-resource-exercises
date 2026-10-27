function verify_practice()
% Execute original topic practice and check signal-processing outcomes.
% This is not a MathWorks Academy submission or assessment of completion.
root = fileparts(mfilename('fullpath'));
previousDirectory = pwd;
previousVisibility = get(groot,'defaultFigureVisible');
cleanup = onCleanup(@() restoreEnvironment(previousDirectory,previousVisibility));
cd(root);
set(groot,'defaultFigureVisible','off');
if ~isfolder('verification'), mkdir('verification'); end
report = struct('status','running','matlab_version',version, ...
    'timestamp',char(datetime('now','TimeZone','UTC')), ...
    'signal_processing_toolbox',logical(license('test','Signal_Toolbox')), ...
    'wavelet_toolbox',logical(license('test','Wavelet_Toolbox')), ...
    'scope','Six original practice scripts; not authenticated Academy exercises.', ...
    'passed_checks',{{}},'metrics',struct());
try
    assert(report.signal_processing_toolbox,'Signal Processing Toolbox license is required.');
    run_all();
    report.passed_checks{end+1} = 'All six practice functions executed.';

    T = readtable('data/synthetic_signal.csv');
    sampleRate = 1/median(diff(T.time_seconds));
    assert(abs(sampleRate-200)<1e-8,'The supplied data must be sampled at 200 Hz.');
    S = load('results/onramp_arrays.mat');
    assert(numel(S.tRegion)==800 && all(diff(S.tRegion)>0));
    assert(all(isfinite(S.xFiltered)) && all(isfinite(S.psd)) && all(S.psd>=0));
    assert(numel(S.psd)==numel(S.f) && S.f(end)<=sampleRate/2+1e-8);
    report.passed_checks{end+1} = 'Onramp: time region, finite filtered signal and nonnegative PSD.';

    R = load('results/resampling_arrays.mat');
    assert(numel(R.resampled)==400 && numel(R.squareResampled)==400);
    assert(numel(R.upsampled)==2000 && numel(R.reconstructed)==2000);
    [P,F] = periodogram(R.aliased70,[],4096,80);
    [~,index] = max(P);
    aliasFrequency = F(index);
    assert(abs(aliasFrequency-10)<0.1);
    highRateAudio = audioinfo('results/upsampled_tone.wav');
    originalAudio = audioinfo('results/original_tone.wav');
    assert(highRateAudio.SampleRate==2*originalAudio.SampleRate);
    assert(abs(highRateAudio.Duration-originalAudio.Duration)<1e-10);
    report.metrics.alias_frequency_hz = aliasFrequency;
    report.passed_checks{end+1} = 'Resampling: sample counts, 70 Hz aliases to 10 Hz at 80 Hz, and audio duration is preserved.';

    S = load('results/spectrum_arrays.mat');
    [~,index] = max(S.amplitude);
    dominantFrequency = S.frequencies(index);
    assert(abs(dominantFrequency-12.3)<0.11);
    names = {'rect','windowed','welch','burg','music'};
    for index = 1:numel(names)
        values = S.(names{index});
        assert(all(isfinite(values)) && all(values>=0));
    end
    report.metrics.dominant_spectral_frequency_hz = dominantFrequency;
    report.passed_checks{end+1} = 'Spectral analysis: 12.3 Hz dominant tone and finite nonnegative spectral estimates.';

    S = load('results/time_frequency_arrays.mat');
    active = S.t>=4 & S.t<4.25;
    assert(all(S.fault(~active)==0) && rms(S.fault(active))>1);
    [b,a] = butter(4,[70 80]/100,'bandpass');
    highBand = filtfilt(b,a,S.x);
    transientRatio = rms(highBand(active))/rms(highBand(S.t>=2 & S.t<3));
    assert(transientRatio>5);
    report.metrics.transient_band_rms_ratio = transientRatio;
    report.passed_checks{end+1} = 'Time-frequency analysis: transient remains localized and detectable in the 70-80 Hz band.';

    S = load('results/filter_arrays.mat');
    M = readtable('results/filter_measurements.csv');
    assert(M.OfflineErrorRMS<M.RawErrorRMS);
    assert(M.LargestPoleMagnitude<1 && all(isfinite(S.offline)));
    interior = T.time_seconds>=0.5 & T.time_seconds<T.time_seconds(end)-0.5;
    expectedWatermark = 0.05*sin(2*pi*35*T.time_seconds);
    watermarkCorrelation = corr(S.recovered(interior),expectedWatermark(interior));
    assert(watermarkCorrelation>0.95);
    [H,F] = freqz(S.specFilter,8192,200);
    worstStopbandDb = max(20*log10(abs(H(F>=40))+eps));
    assert(worstStopbandDb<=-49.9);
    report.metrics.raw_error_rms = M.RawErrorRMS;
    report.metrics.filtered_error_rms = M.OfflineErrorRMS;
    report.metrics.watermark_correlation = watermarkCorrelation;
    report.metrics.worst_stopband_db = worstStopbandDb;
    report.passed_checks{end+1} = 'Filters: stable poles, noise reduction, recovered watermark and specified stopband attenuation.';

    S = load('results/synthetic_wearable_preprocessing.mat');
    assert(isequal(size(S.features),[54 4]));
    assert(sum(S.train)==36 && sum(S.validation)==9 && sum(S.test)==9);
    assert(all(S.train+S.validation+S.test==1));
    assert(isempty(intersect(unique(S.subjectIDs(S.train)),unique(S.subjectIDs(S.validation)))));
    assert(isempty(intersect(unique(S.subjectIDs(S.validation)),unique(S.subjectIDs(S.test)))));
    assert(isempty(intersect(unique(S.subjectIDs(S.train)),unique(S.subjectIDs(S.test)))));
    assert(max(abs(mean(S.normalised(S.train,:),1)))<1e-8);
    assert(max(abs(std(S.normalised(S.train,:),[],1)-1))<1e-8);
    assert(all(isfinite(S.normalised),'all') && all(S.missingRates<=0.05));
    report.passed_checks{end+1} = 'Wearables: disjoint subject splits, 36/9/9 windows, retained quality masks and training-only normalization.';

    report.status = 'passed';
    writeReport(report);
    fprintf('VERIFICATION PASSED: %d checks/groups.\n',numel(report.passed_checks));
catch exception
    report.status = 'failed';
    report.error_identifier = exception.identifier;
    report.error_message = exception.message;
    writeReport(report);
    rethrow(exception);
end
end

function writeReport(report)
fid = fopen(fullfile('verification','results.json'),'w');
assert(fid~=-1,'Cannot write verification report.');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid,'%s\n',jsonencode(report,'PrettyPrint',true));
end

function restoreEnvironment(directory,visibility)
close all force;
set(groot,'defaultFigureVisible',visibility);
cd(directory);
end
