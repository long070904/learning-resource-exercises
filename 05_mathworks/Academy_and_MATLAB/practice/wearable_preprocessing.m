function wearable_preprocessing()
% Original LO1 application: synthetic multimodal signals; not WESAD/Emognition.
if ~isfolder('results'), mkdir('results'); end
rng(42); subjects=6; fs=64; secondsPerRecord=40; window=8*fs; stride=4*fs;
features=[]; subjectIDs=[]; missingRates=[];
for s=1:subjects
    t=(0:1/fs:secondsPerRecord-1/fs)';
    bvp=sin(2*pi*(1+0.04*s)*t)+0.1*randn(size(t));
    edaTime=(0:1/4:secondsPerRecord-1/4)';
    eda=1+0.03*s+0.15*sin(2*pi*.08*edaTime);
    bvp(200:204)=NaN; % a short simulated missing interval
    observed=isfinite(bvp);
    % Preserve a quality mask even when filling values for offline filtering.
    bvp=fillmissing(bvp,'linear');
    [b,a]=butter(3,[.5 8]/(fs/2),'bandpass'); bvp=filtfilt(b,a,bvp);
    edaAligned=resample(eda,fs,4);
    edaAligned=edaAligned(1:numel(t));
    for start=1:stride:numel(t)-window+1
        indices=start:start+window-1; missingRate=mean(~observed(indices));
        if missingRate>.05, continue; end
        block=[bvp(indices),edaAligned(indices)];
        features=[features;mean(block),std(block)]; %#ok<AGROW>
        subjectIDs=[subjectIDs;s]; missingRates=[missingRates;missingRate]; %#ok<AGROW>
    end
end
% Split subjects before fitting learned preprocessing parameters.
train=subjectIDs<=4; validation=subjectIDs==5; test=subjectIDs==6;
mu=mean(features(train,:),1); sigma=std(features(train,:),[],1);sigma(sigma==0)=1;
normalised=(features-mu)./sigma;
assert(isempty(intersect(unique(subjectIDs(train)),unique(subjectIDs(test)))));
assert(all(isfinite(normalised),'all'));
save('results/synthetic_wearable_preprocessing.mat','features','normalised','subjectIDs', ...
    'train','validation','test','mu','sigma','missingRates');
disp(table(sum(train),sum(validation),sum(test),'VariableNames',{'TrainWindows','ValidationWindows','TestWindows'}));
disp('These illustrative cutoffs, windows and missingness thresholds require dataset-specific justification.');
end
