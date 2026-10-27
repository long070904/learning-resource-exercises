# MathWorks Academy progress

## Current completion status — verified 27 October 2026

**Completed — authenticated MathWorks portal verified.** After refreshing
[`My Courses`](https://matlabacademy.mathworks.com/mycourses), the account shows
**Completed (6)**: Signal Processing Onramp; the Core Signal Processing Techniques
in MATLAB pathway; and all four constituent courses (Signal Generation and
Resampling, Spectral Analysis Techniques, Time-Frequency Analysis, and Filter
Design and Analysis Methods). This confirms the student's completion report.
All six official certificate views and their original screenshots have been
saved offline. Original provider PDFs have not been downloaded. Onramp was
completed on 2 October; the complete Core pathway was completed on 27 October.

Both learning-plan allocations are included: Onramp **0.33 CP / 4 estimated hours**
and Core **0.67 CP / 8 estimated hours**, totalling **1 CP / 12 estimated hours**.
The student adopted the 1A planned hours as estimates and extended the reported
study period from **14 September to 27 October 2026**. These are estimates, not
measured study-time logs. The CP allocation records the student's plan-based claim
and does not replace the coordinator's assessment of credit.

See [CURRENT_STATUS_2026-10-27.json](CURRENT_STATUS_2026-10-27.json). The historic
172 graded passes, 28 code examples and 14 GUI activities remain the verified
exercise counts. Native MATLAB startup error **5201** remains unresolved, and
standalone practice replay remains unverified. The Python companion remains a
separate synthetic exercise.

## Historical verified Academy progress — 28 September 2026

The text below is preserved as a dated record. Statements that surveys were
unanswered or that certificates were not claimed describe the September
verification, and are superseded for current status by the refreshed portal above.

Updated 28 September 2026 (Australia/Sydney). Earlier verification dates remain in the JSON history. Results below were observed in signed-in sessions of the hosted Academy grader, not inferred from local execution. The temporary agreement prompt encountered when opening the next course has cleared; its resolution is recorded below.

**All 40 graded Onramp tasks passed.** Seven ungraded code examples and three GUI follow-ups are also verified. The course currently displays **96%**; reaching 100% requires submission of the final survey, whose personal answers remain for the user. No certificate or 100% completion is claimed.

Across the five requested courses, **all 172 graded tasks passed**, with **28 ungraded code examples and 14 GUI activities** verified. Personal surveys for all five courses remain unanswered. Course-specific totals are kept below and in the JSON record.

## Signal Processing Onramp

- Course ID: `signalprocessing`
- [Verified signal-generation lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=1v1&lesson=2&section=1)
- Saved code: [lesson01_generate_signals.m](academy/signalprocessing/lesson01_generate_signals.m)
- [Verified import lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=2v1&lesson=2&section=1): [lesson02_import_signal.m](academy/signalprocessing/lesson02_import_signal.m)
- [Verified power-spectrum lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=2v1&lesson=4&section=1): [03_power_spectrum.md](academy/signalprocessing/03_power_spectrum.md)
- [Verified comparison lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=2v1&lesson=5&section=1): [04_compare_signals.md](academy/signalprocessing/04_compare_signals.md)
- [Verified resampling lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=2&section=1): [05_resample_signals.md](academy/signalprocessing/05_resample_signals.md)
- [Verified region-extraction lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=3&section=1): [06_extract_regions.md](academy/signalprocessing/06_extract_regions.md)
- [Verified custom-preprocessing lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=4&section=1): [07_custom_preprocessing.md](academy/signalprocessing/07_custom_preprocessing.md) and [nm2cm.m](academy/signalprocessing/nm2cm.m)
- [Verified alignment lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=5&section=1): [lesson08_align_signals.m](academy/signalprocessing/lesson08_align_signals.m)
- [Verified spectrum-customization lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=4v1&lesson=2&section=1): [09_customize_spectrum.md](academy/signalprocessing/09_customize_spectrum.md)
- [Verified time-frequency plotting lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=4v1&lesson=4&section=1): [10_time_frequency_plots.md](academy/signalprocessing/10_time_frequency_plots.md)
- [Verified lowpass lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=5v1&lesson=2&section=1): [11_lowpass_filter.md](academy/signalprocessing/11_lowpass_filter.md) and [steepness_comparison.m](academy/signalprocessing/steepness_comparison.m)
- [Verified bandpass lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=5v1&lesson=3&section=1): [12_bandpass_filter.md](academy/signalprocessing/12_bandpass_filter.md)
- [Verified ungraded generated-code lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=1&section=1): [lesson13_generated_code.m](academy/signalprocessing/lesson13_generated_code.m), [preprocess.m](academy/signalprocessing/preprocess.m), and [wanc_spect.m](academy/signalprocessing/wanc_spect.m)
- [Verified measurement lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=2&section=1): [lesson14_signal_measurements.m](academy/signalprocessing/lesson14_signal_measurements.m) and [14_signal_measurements_gui.md](academy/signalprocessing/14_signal_measurements_gui.md)
- Latest course header observed: **96%**, with the final survey open. Earlier observations were 4%, 8%, 12%, 20%, 24%, 28%, 32%, 36%, 40%, 44%, 52%, 60%, 68%, 72%, 76%, and 80%. Navigation and these percentages are not coding-task passes or completion claims.

| Task | Submitted code | Observed grader result |
|---|---|---|
| Generate Signals — 1 | `fs = 100;` then `t = 0:1/fs:1;` | **Correct!** |
| Generate Signals — 2 | `sig = sin(2*pi*5*t);` then `plot(t,sig);` | **Correct!** |
| Generate Signals — 3 | `noise = 0.1*randn(size(sig));` | **Correct!** |
| Generate Signals — 4 | `sigNoisy = sig + noise;` then `plot(t,sigNoisy);` | **Correct!** |
| Generate Signals — 5 | `sq = square(2*pi*5*t);` then `plot(t,sq);` | **Correct!** |
| Import a Signal — 1 | `harp = readmatrix("harp.csv");` then `plot(harp);` | **Correct!** |
| View Power Spectrum — 1 | Drag the course `harp` array into the Signal Analyzer axes. | **Correct!** |
| View Power Spectrum — 2 | Set sample rate to 50 Hz and start time to 0 seconds. | **Correct!** |
| View Power Spectrum — 3 | Enable the spectrum view. | **Correct!** |
| View Power Spectrum — 4 | Set frequency limits to 0–1 Hz. | **Correct!** |
| Compare Signals — 1 | Assign `paxT` as the explicit time vector for `pax`, then show it. | **Correct!** |
| Compare Signals — 2 | Set `wanc` to 100 Hz from 0 seconds, then show it. | **Correct!** |
| Compare Signals — 3 | Show all three signals with spectrum enabled at 0–1 Hz. | **Correct!** |
| Resample Signals — 1 | Duplicate `pax` as `pax_uniform`; resample to 50 Hz with linear interpolation and compare both. | **Correct!** |
| Resample Signals — 2 | Show `wanc` alone with its full 0–50 Hz spectrum. | **Correct!** |
| Resample Signals — 3 | Duplicate `wanc` as `wanc_slow`; resample by a factor of 0.5 and compare both. | **Correct!** |
| Extract Interesting Regions — 1 | Enable the panner and set time limits to 900–1800 seconds. | **Correct!** |
| Extract Interesting Regions — 2 | Extract and display `harp_ROI`, `pax_ROI`, and `wanc_ROI`. | **Correct!** |
| Custom Preprocessing Function — 1 | Duplicate `harp` as `harp_cm`, apply the provided `nm2cm` conversion, and display it. | **Correct!** |
| Custom Preprocessing Function — 2 | Duplicate `pax` and `wanc` as `_cm` signals; apply the same conversion and display all three. | **Correct!** |
| Custom Preprocessing Function — 3 | Export all three `_cm` signals to the MATLAB workspace. | **Correct!**, after exporting the two signals missing from the first attempt. |
| Align Signals — 1 | `[harp,wanc] = alignsignals(harp,wanc);` | **Correct!** |
| Align Signals — 2 | `[pax,wanc] = alignsignals(pax,wanc);` | **Correct!** |
| Customize Power Spectrum Plot — 1 | Display all three signals and their spectra, then use a logarithmic frequency scale. | **Correct!** |
| Create Time-Frequency Plots — 1 | Show `wanc` alone with the default spectrogram. | **Correct!** |
| Create Time-Frequency Plots — 2 | Set spectrogram frequency limits to 2–10 Hz. | **Correct!** |
| Create Time-Frequency Plots — 3 | Set the minimum power limit to −80 dB. | **Correct!** |
| Create Time-Frequency Plots — 4 | Change to the scalogram and retain 2–10 Hz frequency limits. | **Correct!** |
| Create Time-Frequency Plots — 5 | Set the maximum scalogram magnitude to 0.1. | **Correct!** |
| Lowpass Filter — 1 | Copy `wanc` to `wanc_filt`; apply a 0.1 Hz lowpass with default steepness 0.85 and 60 dB stopband attenuation, then compare spectra. | **Correct!** |
| Lowpass Filter — 2 | Display `harp`, `pax`, and `wanc_filt` in time and spectrum views. | **Correct!** |
| Lowpass Filter — 3 | Copy original `wanc` to `wanc_steep`; apply a 0.1 Hz lowpass with steepness 0.95 and compare with `harp` and `pax`. | **Correct!** |
| Bandpass Filter — 1 | Copy `wanc` to `wanc_bandpass`; apply 2–10 Hz bandpass filtering and compare the recordings. | **Correct!** |
| Bandpass Filter — 2 | Display `wanc_lowpass` and `wanc_bandpass` over 180–300 seconds using the panner. | **Correct!** |
| Signal Measurements — 1 | Compute `[p,f,t] = pspectrum(wanc_bandpass,50,"spectrogram");`. | **Correct!** |
| Signal Measurements — 2 | Sum the power across frequency with `psum = sum(p);`, then plot against `t`. | **Correct!** |
| Signal Measurements — 3 | Convert to decibels with `pwr = db(psum,"power");`, then plot against `t`. | **Correct!** |
| Signal Measurements — 4 | Insert the Find Local Extrema Live Editor task for `pwr`, using output `maxIndices` and X-axis `t`. | **Correct!** |
| Signal Measurements — 5 | Configure maxima with minimum prominence 10, minimum separation 0, maximum count 522, and central selection for flat regions. | **Correct!** |
| Signal Measurements — 6 | Extract event times with `quakeSec = t(maxIndices);`. | **Correct!** |

The ungraded follow-up ran `sqNoisy = sq + noise;` and `plot(t,sqNoisy);`. The runtime reported that the section finished and created one output. This is a successful run, not an additional graded pass.

The import lesson's ungraded follow-up ran `harpTT = readtimetable("harp.csv",SampleRate=50);` and `plot(harpTT,"Var1");`. The runtime confirmed completion with one output. Its 50 Hz rate gives a 0.02-second sample interval. The actual `harp.csv` is available in the Academy runtime and has not been downloaded into this package.

The power-spectrum lesson's ungraded follow-up used a data cursor on the spectral peak. The displayed values were **0.05 Hz** and **116.9 dB**, rounded by the app. This was an interactive observation, not an additional grade or a separately calibrated numerical estimate.

For the resampling follow-up, all five signals were shown in time and spectrum views. The spectra for `wanc_slow`, `harp`, and `pax_uniform` ended at 25 Hz; the original `wanc` extended to 50 Hz. The resampled `wanc_slow` had 126000 samples at 50 Hz.

The alignment lesson used the course's `processedsignals.mat`, which is not bundled. Displayed pair delays were `harp/pax = -596`, `harp/wanc = 1167`, and `pax/wanc = 1770`; `wanc` was treated as the latest arrival. The ungraded follow-up loaded the original data into a separate structure and plotted the unaligned recordings for comparison with the existing aligned plot. The runtime confirmed one output. The graded alignment code stayed intact.

The lowpass follow-up executed a command-window comparison using steepness 0.5 and 0.99. Both resulting arrays appeared as 45107×1, the command prompt returned without error, and a Figure 1 tab was created. The figure graphic was obscured by Signal Analyzer, so no visual inspection of that new plot is claimed.

The generated-code lesson was ungraded. Two code examples executed in the hosted command window: the provided `wanc_spect` script and a call to `preprocess(harp,t)` with its resulting plot. Execution returned to the prompt without errors. The HARP plot was visually checked and showed an amplitude on the order of 10⁻³ with edge artifacts. The real `after_filtering.mat` input remains in the course runtime and is not bundled. The provided helper code records an export from MATLAB 9.14 / Signal Processing Toolbox 9.2 dated 23 March 2023.

The measurement lesson's spectrogram outputs had sizes 1024×522 (`p`), 1024×1 (`f`), and 522×1 (`t`). Its live task produced `maxIndices`. A command-window assertion verified that `islocalmax(pwr,MinProminence=10)` exactly matched those indices; the saved script uses that expression. Fourteen event times were displayed and are recorded with the lesson. The ungraded follow-up plotted the actual filtered recording and added vertical lines at `quakeSec`; Academy reported a completed section with one output. The verification assertion does not add another exercise to the counts.

All forty graded Onramp tasks, seven successfully executed ungraded code examples, and three performed ungraded GUI follow-ups are recorded. The bandpass follow-up displayed `harp` and `wanc_bandpass` over 3-5 minutes with the panner enabled and `wanc_lowpass` hidden; the screenshot showed the slow harp wave and bandpass pulses. Adding `harp` autoscaled the amplitude axis, so the earlier -0.2 to 0.2 limits did not persist. Further-practice notes for comparison, custom preprocessing, and spectrum customization were reviewed only; the custom-preprocessing notes discussed timetable export. Reflective questions after time-frequency plotting were read without additional action. The extraction lesson displayed a message permitting progression, with no additional task. These notes, questions, and messages do not count as extra runs or grades.

The summaries for the course overview, earthquake example, Signal Analyzer, preprocessing techniques, frequency analysis, time-frequency analysis, and filtering were reviewed. Their videos were not played. The time-frequency summary introduced spectrograms and scalograms, distinguishing a whole-record spectrum from information about when signal content occurs. The filtering summary covered high-frequency suppression by a lowpass filter and transition-band steepness tradeoffs. The conclusion summary and both signal-processing and MATLAB resource pages were also reviewed.

The final survey asks for the user's own feedback, including how they heard about the course, perceived difficulty, content/recommendation ratings, and comments. It remains unanswered; the last observed submission control was disabled until necessary answers were supplied. The course resource explicitly requires this submission for a 100% indicator. The original survey tab was reused for Signal Generation and Resampling, and the duplicate course tab was closed. The survey is no longer open; [reopen it here](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=7v1&lesson=3&section=1). The task has left that personal feedback to the user and makes no certificate claim.

## Core Signal Processing pathway

**Signal Generation and Resampling** (`otmlsgr`) now has **all 40 graded tasks passed**, plus **6 successful ungraded code examples and 5 performed GUI activities**. Its import lesson passed on 20 September 2026 after the earlier mismatch was resolved. The overview summary was reviewed without playing the video; the learning-outcome and digital-watermarking example texts were also read. Header observations progressed through 4%, 8%, 12%, 20%, 25%, 29%, 37%, 45%, 54%, 62%, 70%, 75%, 79%, 83%, 91%, and **95%**; 95% is the latest verified value, observed after the successful import retry on 20 September. The Resample Signals and Project modules separately displayed 100%, and the personal survey remains unanswered.

### Signal Generation and Resampling: initial signal exercise

[Course source](https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr). Saved code: [lesson01_generate_signal.m](academy/otmlsgr/lesson01_generate_signal.m).

| Task | Submitted code | Grader |
|---|---|---|
| Generate a Signal — 1 | `fs=100;` and `t=0:1/fs:3;` | **Correct!** |
| Generate a Signal — 2 | `sig=sin(2*pi*5*t);` then `plot(t,sig);` | **Correct!** |
| Generate a Signal — 3 | `sig=sig+sin(2*pi*3*t);` then `plot(t,sig);` | **Correct!** |

The ungraded follow-up ran `pspectrum(sig,fs);`; the runtime confirmed a completed section with one output. This is one ungraded code example, not another grader pass.

The next ungraded activity, Generate a Signal (2/2), used the `varyparams.mlx` controls to change amplitude from 1 to 2, frequency from 1 to 3, and phase from 0 to 1.57. Each resulting wave plot was visually checked, and the final Live Script run completed with one output. Its final code was revealed using Output on Right and is preserved in [lesson02_vary_sine_parameters.m](academy/otmlsgr/lesson02_vary_sine_parameters.m). This is counted once as a GUI activity, without an extra graded pass or a second code-example count.

### Import a Signal: recovered and passed

**All 3 tasks passed on 20 September 2026.** Saved GUI record: [13_import_signal.md](academy/otmlsgr/13_import_signal.md). The earlier plot/sample-rate mismatch and failed `signalAnalyzer` workaround are retained as historical troubleshooting only; they add no execution credit.

| Task | Verified final action | Grader |
|---|---|---|
| 1 | Drag `flute` into a fresh GUI and assign 16000 Hz. | **Correct!** |
| 2 | Use the panner for 0–7 seconds, extract `flute_ROI`, rename it `fluteShort`, show both recordings, and restore the full range with Fit to View. | **Correct!** |
| 3 | Enable the spectrum display for `flute` and `fluteShort`. | **Correct!** |

The optional cursor task was performed with a 0-1000 Hz view. The peak readout showed 0.52 kHz, with `fluteShort` at -37.6 dB and `flute` at -37.7 dB. These are rounded UI values, not sub-Hz measurements. Play was invoked with only `fluteShort` visible, and the final UI showed Play enabled and Stop disabled. The completed cursor/playback actions count as one GUI activity. The agent did not hear or assess the audio.

The Sampling Theorem summary under Signal Sampling was reviewed without video playback. Both Analog and Digital Signals slides and two background slides on aliasing were also read.

### Signal Sampling: View Sample Points

Saved source adaptation: [lesson03_view_sample_points.m](academy/otmlsgr/lesson03_view_sample_points.m). These three Live Script tasks received **Correct!**:

| Task | Signal frequency `f` | Sample rate `fs` | Setting demonstrated |
|---|---:|---:|---|
| 1 | 1 Hz | 10 Hz | Sampling above twice the signal frequency. |
| 2 | 1 Hz | 1.5 Hz | Sampling below twice the signal frequency. |
| 3 | 2 Hz | 3 Hz | Aliasing to 1 Hz. |

The ungraded follow-up changed `f` to 3 Hz and `fs` to 4 Hz. Academy reported that `samppts.mlx` finished with two outputs. This counts as one GUI follow-up, without an additional code-example count. The saved `.m` version creates separate waveform and spectrum figures for the tested parameter pairs; that figure arrangement is an adaptation, not a separately executed Academy task.

### Generate a Tone

The two Time Vector slides were reviewed. Saved code for the next activity: [lesson04_generate_tone.m](academy/otmlsgr/lesson04_generate_tone.m). It requires the real course `NoisyFlute.wav`, which is not bundled. The course startup reads the audio, keeps its first seven seconds, and plots its spectrum.

| Task | Submitted operation | Grader |
|---|---|---|
| 1 | Create column sample indices with `t=(0:numel(flute)-1)';`. | **Correct!** |
| 2 | Convert indices to seconds with `t=t/fs;`. | **Correct!** |
| 3 | Generate `wm=sin(2*pi*6000*t);` and plot its spectrum. | **Correct!** |
| 4 | Form `marked=flute+wm;` and plot its spectrum. | **Correct!** |

The ungraded follow-up ran `marked=0.001*wm+flute; pspectrum(marked,fs); soundsc(marked,fs);`. Academy reported a completed section with one output. The audio command executed, but no listening or subjective audio assessment is claimed.

### Generate a Chirp

Saved code: [lesson05_generate_chirp.m](academy/otmlsgr/lesson05_generate_chirp.m). The startup uses the same external course `NoisyFlute.wav`, keeps the first seven seconds, and builds a column time vector.

| Task | Submitted operation | Grader |
|---|---|---|
| 1 | Generate `wm=chirp(t,6000,t(end),7000);` and plot its spectrum. | **Correct!** |
| 2 | Plot the watermark spectrogram with `pspectrum(wm,fs,"spectrogram");`. | **Correct!** |
| 3 | Add the chirp to the flute and plot the resulting spectrum. | **Correct!** |

The ungraded follow-up first plotted the full-amplitude marked signal's spectrogram, then changed the mixture to `marked=flute+0.002*wm;` and plotted another spectrogram. Academy reported a completed section with two outputs. This is one code follow-up; no audio listening or assessment is claimed.

### Effect of Aliasing: Listen to Aliasing

Saved code: [lesson06_listen_to_aliasing.m](academy/otmlsgr/lesson06_listen_to_aliasing.m). Two upsampling slides, two downsampling slides, and two background slides were reviewed. The Aliasing and Imaging video summary was read without playback.

| Task | Accepted operation | Grader |
|---|---|---|
| 1 | `sigbad=downsample(sig,6);` followed by a spectrum at `fs/6`. | **Correct!** |
| 2 | Set `sigfilt=lowpass(sig,fs/12,fs);`, then replace it with `downsample(sigfilt,6)` and plot its spectrum at `fs/6`. | **Correct!**, after correcting the output-variable handling. |

The startup signal combined 300 Hz and 3000 Hz components at 24000 Hz. The first Task 2 attempt used `sigbad`; the hint required `sigfilt` to hold the result after both filtering and downsampling. The recorded final code passed. Conceptual follow-up notes were read only, with no additional execution count or audio-listening claim.

### Decimation of Signals

Saved GUI record: [07_decimation.md](academy/otmlsgr/07_decimation.md). All three tasks received **Correct!**:

| Task | Action performed | Verified result |
|---|---|---|
| 1 | Duplicate `sig` as `sigdect`, resample with sample factor 0.167, then accept and display it. | 2005 samples at 4008 Hz. |
| 2 | Import the provided `sigfilt`, assign 4000 Hz, and display its spectrum with `sigdect` while hiding `sig`. | Comparison display passed. |
| 3 | Export `sigdect` to the MATLAB workspace. | 2005×1 double array. |

This lesson's provided `sigfilt` was a 1×12001 workspace array. It is not represented as the same 2001-element result from the earlier filtering/downsampling task.

The optional GUI playback actions were performed: imported `sigbad` at 4000 Hz, displayed one signal at a time, and pressed the enabled Play control for original `sig` at 24000 Hz, `sigbad` at 4000 Hz, and `sigdect` at 4008 Hz. Each playback started after the previous one was idle. The final controls showed Play enabled and Stop disabled. This counts as one GUI activity. The agent did not hear or analyze the audio, so no subjective listening comparison is claimed and no code-example count is added.

### Effect of Imaging: Listen to Imaging

Both background slides were reviewed. Saved code: [lesson08_listen_to_imaging.m](academy/otmlsgr/lesson08_listen_to_imaging.m). The startup generated a 1200 Hz sinusoid sampled at 3000 Hz. Both tasks received **Correct!**:

| Task | Accepted operation | Grader |
|---|---|---|
| 1 | Set `sigbad=upsample(sig,6);` and plot its spectrum at `fs*6`. | **Correct!** |
| 2 | Set `sigfilt=lowpass(sigbad,fs/2,fs*6);` and plot its spectrum at `fs*6`. | **Correct!** |

The follow-up was explanatory text only and added no execution count. No audio listening or quality assessment is claimed.

### Interpolation of Signals

Saved GUI record: [09_interpolation.md](academy/otmlsgr/09_interpolation.md). All three tasks received **Correct!**:

| Task | Action performed | Verified result |
|---|---|---|
| 1 | Duplicate `sig` as `sigint`, resample with sample factor 6, then accept and display it. | 9006 samples at 18000 Hz. |
| 2 | Import the provided 9006-sample `sigfilt`, assign 18000 Hz, and show its spectrum with `sigint` while hiding `sig`. | Comparison display passed. |
| 3 | Export `sigint` to the MATLAB workspace. | 9006×1 double array. |

For the optional follow-up, imported `sigbad` at 18000 Hz. Displayed one signal at a time and invoked the enabled Play control for original `sig` at 3000 Hz, `sigbad` at 18000 Hz, and `sigint` at 18000 Hz. The final controls showed Play enabled and Stop disabled. These three playback actions count as one GUI activity, not another code example. The agent did not hear the audio or assess its quality.

### Upsample Audio

Saved code: [lesson10_upsample_audio.m](academy/otmlsgr/lesson10_upsample_audio.m), requiring the course `NoisyFlute.wav`. All five tasks received **Correct!**:

| Task | Accepted operation | Grader |
|---|---|---|
| 1 | `fluteup=upsample(flute,2);` | **Correct!** |
| 2 | Set `fsup=2*fs;` and plot the upsampled spectrum at that rate. | **Correct!** |
| 3 | Replace the first operation with `fluteup=resample(flute,2,1);`. | **Correct!** |
| 4 | Build `tup=(0:numel(fluteup)-1)'/fsup;` and generate a chirp from 12000 to 14000 Hz. | **Correct!** |
| 5 | Set `marked=fluteup+0.0001*wm;` and plot its spectrum at `fsup`. | **Correct!** |

The saved script separates the historically accepted zero-insertion stage from the later replacement using `resample`. The optional follow-up ran `soundsc(fluteup,fsup); pause(numel(fluteup)/fsup+0.2); soundsc(marked,fsup);`. Academy reported a completed section with no outputs. This counts as one code follow-up. Both the upsampled audio and the actual watermarked signal were passed to playback commands; the agent did not hear the audio or assess its quality.

### Resample a Watermark

Saved code: [lesson11_resample_watermark.m](academy/otmlsgr/lesson11_resample_watermark.m). This lesson needs the real course `NoisyFlute.wav` and `bird-call-in-spring.mp3`; neither asset is bundled. The startup resampled the flute by 2:1 and set `fsup=fs*2`.

| Task | Accepted operation | Grader |
|---|---|---|
| 1 | Read the bird recording with `[birds,fsb]=audioread("bird-call-in-spring.mp3");` and plot its spectrum. | **Correct!** |
| 2 | Convert channels to mono with `birds=mean(birds,2);`. | **Correct!** |
| 3 | Compute the rational rate ratio with `[p,q]=rat(fsup/fsb);`. | **Correct!** |
| 4 | Set `birdsdown=resample(birds,p,q);` and plot its spectrum at `fsup`. | **Correct!** |

The optional follow-up ran `soundsc(birds,fsb); pause(numel(birds)/fsb+0.2); soundsc(birdsdown,fsup);`. Academy reported a completed section with no outputs. This counts as one code follow-up. Playback commands used the respective sample rates; the agent did not hear or assess the audio. Separate figures were added in the saved script to preserve its spectra outside the Live Editor, without altering the verified computations.

### Project: Generate and Resample a Square Wave

Saved code: [lesson12_square_wave.m](academy/otmlsgr/lesson12_square_wave.m) and the course-provided [sumOddHarmonics.m](academy/otmlsgr/sumOddHarmonics.m). All five project tasks received **Correct!**:

| Task | Accepted operation | Grader |
|---|---|---|
| 1 | Set `fs=100;` and `t=(0:1/fs:3)';`. | **Correct!** |
| 2 | Create `y1=sin(2*pi*t);`. | **Correct!** |
| 3 | Create `y3=sin(2*pi*3*t)/3;` and plot `y1+y3`. | **Correct!** |
| 4 | Set `fsup=200;` and compute `[p,q]=rat(fsup/fs);`. | **Correct!** |
| 5 | Set `squareup=resample(y1+y3,p,q);` and plot its spectrum at `fsup`. | **Correct!** |

The ungraded follow-up ran `sumOddHarmonics(10)` and completed with one output. The supplied helper's source was opened and reviewed; the saved helper preserves its computations and adds a valid closing `end`. The saved driver uses separate figures to retain plots outside the Live Editor. These display adaptations do not add verification credit. The earlier import gap has now been resolved, so no graded task remains outstanding in this course.

The concluding summary, all four Signal Analyzer workflow slides, and next-step resources were reviewed. The [final survey](https://matlabacademy.mathworks.com/v1/portal.html?course=otmlsgr#chapter=5v1&lesson=3&section=1) was left unanswered for the user's personal ratings. All graded work and the recorded optional follow-ups are verified. Full course completion and a certificate have not been claimed.

Time-Frequency Analysis has all twenty-four graded tasks passed; Filter Design and Analysis Methods has all thirty-seven graded tasks passed. All four pathway courses remain in scope; their public outlines are listed in [COURSE_MAP.md](COURSE_MAP.md).

## Spectral Analysis Techniques

The course (`otmlsat`) has **all 31 graded tasks passed**, with **5 ungraded code examples and 2 ungraded GUI activities**. Its latest observed header is **96%** on 25 September, with the personal survey unanswered. Historical header observations through 78% on 20 September and 85% and 89% on 25 September are retained in the JSON record. The overview video page was visited, but neither playback nor summary review is claimed. All three Fourier slides and both Number of DFT Points slides were read. The Is FFT Enough and Windowing video summaries were reviewed without playback, along with the windowing background material.

The ungraded healthy-fan example ran `genfansig.mlx` and completed with one output. Saved code: [lesson01_generate_fan_signal.m](academy/otmlsat/lesson01_generate_fan_signal.m). The example uses 2400 samples at 2400 Hz and a rotation rate of 4000 rpm, or approximately 66.67 Hz. Course reference fault frequencies are 211.96 Hz (ball), 256.87 Hz (inner race), 143.13 Hz (outer race), and 23.85 Hz (cage); these are background values, not measured detection results.

The FFT exercise loads the course `psdsig.mat`, which is not bundled. Its displayed workspace includes scalar `fr`, `fs`, and `n`, with 2400×1 `sig` and `t`. Saved code: [lesson02_fft.m](academy/otmlsat/lesson02_fft.m). All five tasks received **Correct!**:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `Y=fft(sig);` | **Correct!** |
| 2 | `n=length(sig);` | **Correct!** |
| 3 | `f=(0:n-1)*(fs/n);` | **Correct!** |
| 4 | `p=abs(Y).^2; plot(f,p);` | **Correct!** |
| 5 | `plot(f,10*log10(p));` | **Correct!** |

The follow-up involved conceptual inspection of the existing plots: three lower-frequency peaks had mirrored peaks at the high-frequency end. No extra code or GUI activity is counted. Named figures in the saved script preserve both plots outside the Live Editor; that display arrangement is an adaptation, not an additional verified run.

### Calculate the Periodogram

Saved code: [lesson03_periodogram.m](academy/otmlsat/lesson03_periodogram.m). The startup loads the course `psdsig.mat`, then replaces `sig` with a single sinusoid at `fr` and obtains its sample count. All five tasks received **Correct!**:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `w=ones(n,1);` | **Correct!** |
| 2 | `nfft=n;` | **Correct!** |
| 3 | `periodogram(sig,w,nfft,fs);` | **Correct!** |
| 4 | `periodogram(sig,[],[],fs);` | **Correct!** |
| 5 | `[p,f]=periodogram(sig,w,nfft,fs); plot(f,p);` | **Correct!** |

The follow-up provided conceptual guidelines only and added no executed example. Separate figures in the saved script preserve the three displays; the display arrangement is an adaptation, with the accepted computations unchanged.

### Find Frequency Spikes

Saved code: [lesson04_frequency_spikes.m](academy/otmlsat/lesson04_frequency_spikes.m), requiring the course `psdsig.mat`. The startup constructs a single sinusoid, calculates its periodogram using the signal-length transform, and plots its decibel values with point markers. Both tasks received **Correct!**:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `[peak,loc]=findpeaks(pwr,f,NPeaks=1,SortStr="descend");` | **Correct!** |
| 2 | `e=abs(fr-loc);` | **Correct!** |

The follow-up was conceptual only, with no additional code or GUI activity counted.

### Improve Precision

Saved code: [lesson05_precision.m](academy/otmlsat/lesson05_precision.m), requiring `psdsig.mat`. The single graded slider task received **Correct!** after setting the exponent to 18, giving `nfft=262144`. The displayed peak location was **66.6687 Hz** and its absolute error was **0.0020 Hz**; these are rounded display values.

The slider-triggered run completed with six outputs. It counts only as the one graded task, not an additional ungraded code or GUI activity. The conceptual follow-up recommended `2^12` transform points for remaining course work; that recommendation is not another execution.

### Create and Apply Windows

All five tasks received **Correct!**. [GUI evidence](academy/otmlsat/lesson06_windows_gui.md) records the actual Window Designer settings and exports. [lesson06_windows.m](academy/otmlsat/lesson06_windows.m) provides a plain-code replay of those settings; it is an adaptation, not a claim that the replay script passed GUI checks.

| Task | Verified action | Grader |
|---|---|---|
| 1 | Create rectangular window `w`, length 2400, in Window Designer; apply and save to the workspace, then plot it against `t`. | **Correct!** |
| 2 | Run `periodogram(sig,w,2^12,fs);`. | **Correct!** |
| 3 | Replace `w` through Window Designer with a Hamming window of length 2400. | **Correct!** |
| 4 | Replace `w` with a Kaiser window of length 2400 and beta 1. | **Correct!** |
| 5 | Change the Kaiser beta to 20 and save `w` again. | **Correct!** |

The ungraded `compwindows.mlx` comparison ran successfully with two outputs and counts once as a code example. Its saved [compwindows.m](academy/otmlsat/compwindows.m) uses separate figures and preserves the supplied `10*log10(abs(h))` expression and its “Power (dB)” label. That inherited display is not represented as a calibrated PSD or silently changed to another normalization. The five graded GUI operations are not additional ungraded GUI activities.

### Resolve Tiny Tones

The single graded task received **Correct!** with Kaiser beta set to 10. The screenshot showed three peak markers aligned with the reference-frequency lines. Saved calculation: [lesson07_tiny_tones.m](academy/otmlsat/lesson07_tiny_tones.m).

The separate ungraded GUI practice applied a 64-sample rectangular window and a 64-sample Kaiser window with beta 10 in Window Designer, then selected both to compare their time and frequency displays. Both overlays were visually verified. [The GUI record](academy/otmlsat/lesson07_tiny_tones_gui.md) preserves these settings. This counts as one GUI activity. All three Compare Different Windows slides were read.
### Resolve Closely Spaced Tones

The single graded task received **Correct!** with Kaiser beta set to 0 for the 25 Hz and 26 Hz tones. The screenshot showed both peak markers aligned with the reference lines. Saved calculation: [lesson08_close_tones.m](academy/otmlsat/lesson08_close_tones.m). The further-practice notes were conceptual only; no additional execution or GUI activity is counted. The header observed at that stage was 53%.
### Welch Method

The Noisy Signals introduction was reviewed, and the Spectrum of Noisy Signals video summary was read without playback. Saved code: [lesson09_welch.m](academy/otmlsat/lesson09_welch.m), requiring the course `psdsig.mat`. All four tasks received **Correct!**:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `w=ones(n,1); nfft=2^12;` | **Correct!** |
| 2 | `numoverlap=0;` | **Correct!** |
| 3 | `pwelch(sig,w,numoverlap,nfft,fs);` | **Correct!** |
| 4 | `pwelch(sig,[],[],[],fs);` | **Correct!** |

The follow-up was conceptual only and added no execution count. The saved script adds separate named figures without changing the accepted calculations.
### Decrease Window Length

All four slider tasks received **Correct!** with `numsegments` set to **2, 3, 15, and 20**, respectively. The course loaded `brokenouterrace.mat` and displayed `n=12000`. Each setting used `winlen=n/numsegments`, a Kaiser window with beta 19 and rounded length, no overlap, and `2^12` transform points.

Saved replay: [lesson10_window_length.m](academy/otmlsat/lesson10_window_length.m). Its independent-figure loop is a standalone adaptation of the verified settings, not another executed example. The real course MAT file is not bundled.

Both background slides and the final background text were read. The latter described a noise level around -45 to -40 dB and merging of the first two tones; these are course-explanation details, not new numerical measurements. The conceptual follow-up added no code or GUI activity. The header was observed at 67% before lesson completion.
The Downsides of Welch Method page was reviewed, with the header observed at 75%.

### Increase Overlap

The single graded slider task received **Correct!** at overlap fraction **0.5**. The course loaded `brokenouterrace.mat`, divided the sample count into five windows, and used a Kaiser window with beta 19. Saved code: [lesson11_overlap.m](academy/otmlsat/lesson11_overlap.m).

The ungraded follow-up changed the fraction to **0.8**, producing `numoverlap=1920` for `winlen=2400`. It replotted the Welch estimate and added `[2*fr frO 2*frO 3*frO 4*frO 5*frO]` as reference lines using the course's `loc/1000` plotting conversion. Academy reported a completed section with one output, and a screenshot confirmed six vertical overlays. This counts as one code example. The course header at that stage was observed at 78%.
### Parametric Methods

On 25 September, the sample-count task received **Correct!** after comparing the `n=20`, `n=30`, and `n=50` plots and submitting **`n=50`**. The supplied signal contains 200 Hz and 250 Hz tones sampled at 2000 Hz, with reproducible Gaussian noise. The course compares an order-8 Burg estimate with a periodogram, both using `2^10` frequency points. The resumed course header displayed 85%.

The ungraded further practice added `pyulear(y,8,2^10,fs)`, `pcov(y,8,2^10,fs)`, and `pmcov(y,8,2^10,fs)` after the Burg call. Academy reported a completed section with five outputs, including the two original comparisons. This counts as **one** ungraded code activity. Saved code: [lesson12_parametric.m](academy/otmlsat/lesson12_parametric.m). Its separate named figures preserve all five plots; the standalone display arrangement has not been independently executed.

### Subspace Methods

On 25 September, the single graded task received **Correct!** with a duration of **0.5 seconds**, producing **501 samples**, and `numtones=6`. The signal contains 100 Hz, 200 Hz, and 220 Hz components sampled at 1000 Hz, with reproducible noise. The provided code compares eigenvector, Welch, and periodogram estimates. The course header displayed 89%.

For the ungraded GUI practice, the `numtones` control was changed to 10. Academy reported a completed run with four outputs; the screenshot showed extra spurious peaks. The control was then restored to 6. This counts as one GUI activity.

The provided Try MUSIC example was separately run by uncommenting `pmusic(xn,numtones,2^10,fs)`. Academy reported a completed section with three outputs, counted as one ungraded code activity. [lesson13_subspace.m](academy/otmlsat/lesson13_subspace.m) preserves the signal, comparisons, and optional parameter experiment in separate figures; that standalone arrangement has not been independently executed. All 31 graded activities in the course have passed.

The conclusion summary, its two zero-padding slides and three windowing slides, and the Next Steps resources were reviewed on 25 September. The [final survey](https://matlabacademy.mathworks.com/v1/portal.html?course=otmlsat#chapter=8v1&lesson=3&section=1) remains unanswered for the user's personal ratings. The latest course header is 96%; no 100% completion or certificate is claimed. Time-Frequency Analysis followed this course; its verified results are recorded below.

## Time-Frequency Analysis

The course (`otmltfa`) has **all 24 graded tasks passed**, no additional code examples, and **1 ungraded GUI activity**. The latest observed header is **95%** on 25 September, with its personal survey unanswered. The overview page was visited only; neither video playback nor summary review is claimed. Outcomes and prerequisites, the Gear Box example, and the Time-Varying Signals introduction were reviewed.

### Time-Varying Gear Box Signal

Both tasks received **Correct!** on 25 September:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `pspectrum(healthyGear,fs);` | **Correct!** |
| 2 | `pspectrum(monitoredGear,fs);` | **Correct!** |

The course setup loaded `monitoredgearbox.mat`; the workspace displayed `healthyGear` as 1×15000, `monitoredGear` as 1×40000, and `fs` as a scalar. No sampling-rate value is inferred from introductory material. The real MAT file is required and is not bundled. Saved code: [lesson01_gear_spectra.m](academy/otmltfa/lesson01_gear_spectra.m), with separate named figures as an unexecuted standalone display adaptation. Further practice was conceptual only and added no activity count.

### Effect of Window Length on Spectrogram

In the ungraded `spectropara.mlx` activity, the window-length control was changed from 260 to **500**. Academy reported a completed run with one output, and the screenshot showed separated 25 Hz and 26 Hz bands. This counts as **one GUI activity**, with no additional graded pass or code-example count. [lesson02_window_length.m](academy/otmltfa/lesson02_window_length.m) saves the revealed calculation with the verified 500-sample Hamming window; the standalone replay has not been independently executed.

The Time-Frequency Visualizations video summary and the Spectrogram Function input page were reviewed. The video was not played. The latest observed header was 40%.

### Spectrogram Function

All three tasks received **Correct!** on 25 September. The setup loaded `monitoredgearbox.mat` and displayed `n=40000` samples in `monitoredGear`.

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `spectrogram(monitoredGear,ones(n,1),0,[],fs);` | **Correct!** |
| 2 | `spectrogram(monitoredGear,[],[],[],fs);` | **Correct!** |
| 3 | `spectrogram(monitoredGear,[],[],[],fs,"yaxis");` | **Correct!** |

[lesson03_spectrogram.m](academy/otmltfa/lesson03_spectrogram.m) preserves the three comparisons with separate named figures; that standalone arrangement has not been independently executed. The course MAT file remains an external requirement. Further practice reviewed the defaults conceptually and added no executed activity.

### Time Resolution

Both tasks received **Correct!** on 25 September: `w=hamming(2500);`, followed by `spectrogram(monitoredGear,w,[],[],fs);`. The course starting display used default spectrogram parameters on `monitoredgearbox.mat`. [lesson04_time_resolution.m](academy/otmltfa/lesson04_time_resolution.m) saves both comparisons in separate figures as a standalone display adaptation.

Further practice was conceptual only. The course feedback states that additional frequencies appear at 3 seconds; that is supplied explanatory feedback, not a new numerical measurement. No extra activity is counted. The header was observed at 45% before lesson completion.

### Spectrogram Matrix

All three tasks in `gearspecmatrix.mlx` received **Correct!** on 25 September:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `[s,f,t,ps] = spectrogram(monitoredGear,hamming(2500),[],[],fs)` | **Correct!** |
| 2 | `firstslice = ps(:,1); plot(f,firstslice)` | **Correct!** |
| 3 | `lastslice = ps(:,end); plot(f,lastslice)` | **Correct!** |

The displayed outputs were `s` 2049×31 complex, `f` 2049×1, `t` 1×31, and `ps` 2049×31. [lesson05_spectrogram_matrix.m](academy/otmltfa/lesson05_spectrogram_matrix.m) requires the unbundled `monitoredgearbox.mat`. Its replay uses separate figures and suppresses the large matrix display with a semicolon; these are display adaptations, not additional verified runs.

The conceptual follow-up describes an initially healthy signal followed by an added 2 kHz fault component. This is course feedback and adds no activity count. The observed course header was 55%.

### Time-Frequency Analysis - Scalogram

Both tasks in `gearscal.mlx` received **Correct!** on 25 September:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `cwt(monitoredGear,fs);` | **Correct!** |
| 2 | `cwt(monitoredGear,fs,FrequencyLimits=[1 2500]);` | **Correct!** |

[lesson06_scalogram.m](academy/otmltfa/lesson06_scalogram.m) requires **Wavelet Toolbox** and the unbundled course `monitoredgearbox.mat`. Separate figures retain the full-range and limited-range scalograms as a standalone adaptation. During a revisit, the later Task 2 plot was temporarily commented so that whole-file execution would not replace Task 1's display; Task 1 was reverified as Correct, then Task 2 was restored and resubmitted with another Correct result. The record preserves the individually observed passes, not an inferred whole-file pass.

The scalogram/CWT and wavelet concept pages were reviewed. The follow-up offered progression only and added no activity. The latest header was 70%.

### Improve Frequency Resolution

The single task in `gearfreqres.mlx` received **Correct!** on 25 September with `cwt(monitoredGear,"bump",fs);`. The starting display used the default wavelet. [lesson07_frequency_resolution.m](academy/otmltfa/lesson07_frequency_resolution.m) preserves both comparisons in separate figures and requires Wavelet Toolbox and the unbundled `monitoredgearbox.mat`.

The follow-up offered progression only, so no ungraded activity is counted. The latest observed header was 75%.

### Scalogram Matrix

All four tasks in `scalmatrix.mlx` received **Correct!** on 25 September:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `[w,f] = cwt(monitoredGear,"bump",fs)` | **Correct!** |
| 2 | `p=abs(w).^2;` | **Correct!** |
| 3 | `firstslice=p(:,1); plot(f,firstslice)` | **Correct!** |
| 4 | `lastslice=p(:,end); plot(f,lastslice)` | **Correct!** |

The displayed coefficient matrix `w` was 110×40000 complex. [lesson08_scalogram_matrix.m](academy/otmltfa/lesson08_scalogram_matrix.m) requires Wavelet Toolbox and the unbundled `monitoredgearbox.mat`. Its semicolon suppresses the large coefficient display, and separate figures retain both slices; these replay adaptations have not been independently executed.

Further practice was conceptual feedback about the 2 kHz fault component and added no activity count. The latest observed header was 80%.

### Project: Identify Fan Faults

All seven tasks in `project.mlx` received **Correct!** on 25 September:

| Task | Accepted code | Grader |
|---|---|---|
| 1 | `spectrogram(monitoredfan,[],[],[],fs);` | **Correct!** |
| 2 | `w=kaiser(2048,19); spectrogram(monitoredfan,w,[],[],fs);` | **Correct!** |
| 3 | `ylim([3 5]);` | **Correct!** |
| 4 | `[s,f,t,ps] = spectrogram(monitoredfan,w,[],[],fs)` | **Correct!** |
| 5 | `firstslice=ps(:,1); plot(f,firstslice)` | **Correct!**, after an unchanged-code retry cleared a transient Live Editor line-number error. |
| 6 | `lastslice=ps(:,end); plot(f,lastslice)` | **Correct!** |
| 7 | `cwt(monitoredfan,"bump",fs);` | **Correct!** |

The course workspace showed `fs=2400`, `monitoredfan` 30001×1, `n=30001`, `fr=66.6667`, `frO=143.1300`, and `frR=211.9600` at displayed precision. [lesson09_fan_fault_project.m](academy/otmltfa/lesson09_fan_fault_project.m) requires the unbundled `monitoredfan.mat`, Signal Processing Toolbox, and Wavelet Toolbox. Its separate figures retain each comparison, with Task 3's time limits still attached to Task 2's plot; a semicolon suppresses Task 4's large output. The replay arrangement has not been independently executed.

The conceptual feedback identifies the strongest component near 573 Hz as a harmonic of the outer-race frequency, indicating a broken outer race. The explanation quotes approximately 143.14 Hz while the workspace displayed 143.13 Hz. These are supplied course values and conclusions, not a new measured diagnosis. No ungraded activity is counted. The header at the project stage was 85%.

The conclusion summary and Next Steps were reviewed on 25 September. The Project and Wavelet module dialogs each showed 100%, while the course header showed 95%. The [final survey](https://matlabacademy.mathworks.com/v1/portal.html?course=otmltfa#chapter=6v1&lesson=3&section=1) remains unanswered for the user's personal responses. All 24 graded tasks and the one optional GUI activity are verified; no 100% course completion or certificate is claimed.

## Filter Design and Analysis Methods

The course (`otmlfdam`) has **all 37 graded tasks passed**, **10 ungraded code examples**, and **3 ungraded GUI activities**. Its latest observed header is 96%, with the personal survey unanswered. The introduction, four filter-configuration slides, and introductory video summaries were reviewed; no video playback is claimed.

### Interactively Design a Filter

All three tasks in `flutesetuptask.mlx` received **Correct!** on 25 September. The first inserted the Design Filter Live Editor task with **Bandpass FIR defaults** and output `designedFilter`. The next applied `yout=filter(designedFilter,marked);`, followed by `pwelch(yout,[],[],[],fs);`.

The task's Show Code view was inspected. Its generated `designfilt` call uses normalized edges 0.35, 0.45, 0.55, and 0.65; 60 dB attenuation in both stopbands; and 1 dB passband ripple. The generated response display calls `freqz(designedFilter)`. [The GUI record](academy/otmlfdam/lesson01_design_filter_gui.md) and [lesson01_design_filter.m](academy/otmlfdam/lesson01_design_filter.m) preserve the verified operations. The script requires Signal Processing Toolbox and the unbundled `NoisyFlute.wav`; it is a replay of observed generated code and accepted calculations with separate figures, not an independently executed GUI-grader result.

The conceptual follow-up and its optional repetition of graded code add no ungraded activity count.

### Design an FIR Filter

All three tasks in `flutefiltpassstop.mlx` received **Correct!** on 25 September. The Design Filter task was switched to Hz with sample rate `fs`; its minimum-order FIR bandpass edges were set to 2100, 2200, 2500, and 2600 Hz; then the lower-stopband attenuation was set to 80 dB, retaining 1 dB passband ripple and 60 dB upper-stopband attenuation. The observed generated code used `SampleRate=16000`.

For one ungraded GUI activity, Filter Information showed length **425** at 80 dB lower-stopband attenuation, **317** after changing it to 60 dB, and **425** after restoring 80 dB. The stronger attenuation therefore adds 108 coefficients; the corresponding orders are 424 and 316.

A separate ungraded code activity ran `soundsc(yin,fs); pause(3.5); soundsc(yout,fs);`. Academy reported a completed section with no outputs. Playback commands executed, but no claim is made that the agent heard or assessed the audio.

[lesson02_fir_filter.m](academy/otmlfdam/lesson02_fir_filter.m) and [the GUI record](academy/otmlfdam/lesson02_fir_filter_gui.md) preserve the final 80 dB setting, generated design code, comparisons, and playback. The replay requires the unbundled `NoisyFlute.wav` and Signal Processing Toolbox. The standalone figure arrangement has not been independently executed. The latest header was 21%.

### Design an IIR Filter

Both tasks in `flutefiltiir.mlx` received **Correct!** on 25 September. The task was set to Bandpass IIR with Hz units, sample rate `fs`, and output `designedFilter`; the automatically chosen `designedFilter2` name was corrected. The minimum-order design edges were then set to 2100, 2200, 2500, and 2600 Hz.

The Show Code view used 60 dB attenuation in each stopband, 1 dB passband ripple, `SampleRate=16000`, and `ScaleSOS=true`. [lesson03_iir_filter.m](academy/otmlfdam/lesson03_iir_filter.m) and [the GUI record](academy/otmlfdam/lesson03_iir_filter_gui.md) preserve the generated design and downstream filtering. Signal Processing Toolbox and the unbundled `NoisyFlute.wav` are required. The standalone display arrangement has not been independently executed. The optional playback ran `soundsc(yin,fs); pause(3.5); soundsc(yout,fs);`. Academy reported a completed section with no outputs, with Stop disabled. This adds one code activity; no listening or subjective audio comparison is claimed. The latest header was 28%.

### Design a Filter Using Filter Designer

One ungraded GUI workflow was completed on 25 September. In Filter Designer, a Bandpass FIR design used Algorithm → Window → Rectangular, sample rate 16000 Hz, specified order 200, and 6 dB cutoffs 2200 and 2500 Hz. The task allowed an order choice. After Update Filter, coefficients were exported to the MATLAB Workspace and Designer was closed. The workspace showed `bandpassfir1_Num` as a 1×201 double.

The integrated commands `yout=filter(bandpassfir1_Num,1,marked); pwelch(yout,[],[],[],fs);` executed and the Command Window prompt returned. These steps belong to the same GUI activity and do not add a separate code-example count.

A reconstruction check with `bReplay=fir1(200,[2200 2500]/(fs/2),rectwin(201));` returned **0** for `max(abs(bReplay-bandpassfir1_Num))`. [lesson04_filter_designer.m](academy/otmlfdam/lesson04_filter_designer.m) uses this verified equivalent reconstruction, and [the GUI record](academy/otmlfdam/lesson04_filter_designer_gui.md) preserves the design/export workflow. The full standalone replay has not been independently executed. The latest header was 37%.

### Impulse Response

Both tasks in `fluteimp.mlx` received **Correct!** on 25 September. Impulse Response was selected for `designedFIR` and `designedIIR` in their Design Filter tasks. The FIR used the earlier 80/1/60 dB specifications and exposed `freqz(designedFIR,[],fs); impz(designedFIR,[],fs);`. The IIR retained its 60/1/60 dB specifications and `ScaleSOS=true`, with `impz(designedIIR,[],fs);` exposed in generated code.

[lesson05_impulse_response.m](academy/otmlfdam/lesson05_impulse_response.m) and [the GUI record](academy/otmlfdam/lesson05_impulse_response_gui.md) preserve the designs and analyses with separate figures. The conceptual follow-up discusses automatic selection of the IIR response length and adds no activity. The latest header was 43%.

### Compute Frequency Response

The single task in `flutefreqz.mlx` received **Correct!** on 25 September after selecting **Display filter response → Group delay** for `designedFIR`. The accepted `designedFIR` retains the earlier 80/1/60 dB specifications; its generated analysis calls are `freqz(designedFIR,[],fs);` and `grpdelay(designedFIR,[],fs);`. Course feedback describes a constant delay of **212 samples**; this is supplied feedback, not a new measured result.

One ungraded code example then ran `[h,f]=freqz(designedFIR,[],fs); plot(f,abs(h));`. Academy reported a completed section with one output. [lesson06_frequency_response.m](academy/otmlfdam/lesson06_frequency_response.m) preserves the design, analyses, and example using separate figures as a standalone adaptation. The latest header was 46%.

### Filter Analyzer App

One ungraded GUI comparison in `filtanaly.mlx` was completed on 25 September. The `filterAnalyzer` launch section completed with no outputs. Both `designedFIR` and `designedIIR` were imported through Filter Objects and verified as 16 kHz rows. The Group Delay view showed the FIR's constant **212-sample delay** and a nonconstant IIR delay with peaks around **2.2 and 2.5 kHz**. Both filters were also displayed in the Phase view before the app was closed.

The launch belongs to this GUI activity and adds no separate code-example count. [lesson07_filter_analyzer.m](academy/otmlfdam/lesson07_filter_analyzer.m) retains the original setup and launch, and [the GUI record](academy/otmlfdam/lesson07_filter_analyzer_gui.md) documents the manual comparison. Both provided designs use `SampleRate=fs`; this lesson's IIR call has no `ScaleSOS` argument. The latest header was 50%.

### Remaining filter lessons completed on 28 September

Every graded task listed below returned **Correct!** in the authenticated Academy grader. The group-delay Task 1 was also rechecked after restoring the session; it is counted only once. Separate figures and repeated calculations in saved scripts preserve successive results and are standalone adaptations, not separately executed native MATLAB runs.

| Lesson | Graded passes | Additional code examples | Saved code |
|---|---:|---:|---|
| Compensate for Group Delay | 4 | 0 | [lesson08_group_delay.m](academy/otmlfdam/lesson08_group_delay.m) |
| Zero-Phase Filtering | 1 | 0 | [lesson09_zero_phase.m](academy/otmlfdam/lesson09_zero_phase.m) |
| FIR Filter Transient | 4 | 2 | [lesson10_fir_transient.m](academy/otmlfdam/lesson10_fir_transient.m) |
| IIR Filter Transient | 2 | 1 | [lesson11_iir_transient.m](academy/otmlfdam/lesson11_iir_transient.m) |
| Create Desired Absorption Filter | 2 | 1 | [lesson12_absorption_response.m](academy/otmlfdam/lesson12_absorption_response.m) |
| Arbitrary Filter Response | 6 | 1 | [lesson13_arbitrary_filter.m](academy/otmlfdam/lesson13_arbitrary_filter.m) |
| FIR Zero-Pole Plot | 2 | 0 | [lesson14_fir_poles.m](academy/otmlfdam/lesson14_fir_poles.m) |
| Reduce FIR Filter Delay | 3 | 1 | [lesson15_minimum_phase.m](academy/otmlfdam/lesson15_minimum_phase.m) |
| IIR Filter Stability | 2 | 1 | [lesson16_iir_stability.m](academy/otmlfdam/lesson16_iir_stability.m) |

The optional runs covered FIR transient zoom/trimming, the supplied [filter-to-zero example](academy/otmlfdam/lesson10_filter_to_zero.m), IIR transient zoom/playback, absorption-plot labels, whale-audio playback, phase-property checks, and high-order IIR stability plots. Playback commands executed; no listening or subjective audio assessment is claimed. Both phase checks returned logical 1.

The supplied `filtertozero.mlx` could not restore its old Design Filter control. Converting that control to its displayed code preserved the design; all three expected plots appeared. The high-order IIR exercise intentionally produced rank-deficiency warnings and a filtered signal plotted on a 10^304 scale. Its two optional plots completed. A transient Live Editor line-number error during group-delay grading cleared after running the section and resubmitting.

Filter Analysis, Arbitrary Response Filter Design and Analysis, and Filter Stability each showed **100%** in their module-completion dialogs. The course summary and next steps were reviewed. The [final survey](https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=7v1&lesson=3&section=1) is open and unanswered; the course header is **96%**. MathWorks states that submitting the survey is required for 100% course completion.

The new scripts require Signal Processing Toolbox as applicable. Flute lessons need the course `NoisyFlute.wav`; underwater lessons need `whalesound.wav` and the course's simplified `absorption.m`. Those external assets are not bundled. The filter-to-zero example uses a generated signal and needs no course data file.

## Exercise completion and resolved access prompt

All five requested courses now have their graded exercises passed and conclusions reviewed. **Filter Design and Analysis Methods finished with 37 graded passes and a 96% header on 28 September**. Personal surveys remain for the user. The landing page displayed access through 30 January 2027. After Spectral Analysis was finished on 25 September, opening Time-Frequency Analysis temporarily redirected to the [MathWorks agreement acceptance page](https://www.mathworks.com/mwaccount/account/incomplete/acceptance) for the updated [Online Services Agreement](https://www.mathworks.com/company/aboutus/policies_statements/online-services-agreement.html).

The user explicitly authorized acceptance. Before the agent could click Accept, the prompt had gone and the MATLAB homepage was active; **acceptance by the agent is not claimed**. Navigation to Time-Frequency Analysis then succeeded, displaying 0% and an available Start Course button. The access interruption was resolved and all requested exercise work subsequently finished. Navigation alone adds no exercise passes.

## Runtime evidence

The hosted Academy runtime produced the course-specific grades and follow-up results above. An earlier native MATLAB startup attempt on this computer failed with service error 5201 before running the independent practice scripts. These are separate execution environments.
