# MathWorks course map

## Current completion — verified 27 October 2026

The refreshed authenticated [MathWorks My Courses](https://matlabacademy.mathworks.com/mycourses)
page shows **Completed (6)**: Onramp, the Core pathway and all four Core courses.
See [CURRENT_STATUS_2026-10-27.json](CURRENT_STATUS_2026-10-27.json) and the
[current guide](README.md). All six official certificate views and their original screenshots are saved offline. Original provider PDFs have not been downloaded.
The two plan allocations total **1 CP (0.33 + 0.67)** and **12 estimated hours
(4 + 8)**, with the student-reported study period ending 27 October.

## Historical course-outline inventory and September observations

The survey-pending/header observations and completion flags below are the
original September record. They do not describe the refreshed current account.

Public outlines checked on 19 September 2026. The two resource links cover one introductory course and a pathway containing four further courses. The [MathWorks announcement](https://www.mathworks.com/matlabcentral/discussions/highlights/875537-new-online-training-courses) confirms that grouping.

The entries below paraphrase the public module topics, in course order. A module is not an exercise: the public pages do not disclose each graded task, its required variables, its data, or its expected output. This map is an outline inventory. Verified authenticated work is now recorded separately in [ACADEMY_PROGRESS.md](ACADEMY_PROGRESS.md), which is the current source for individual task results. No certificate completion is claimed.

| Course | Public module topics, in order | Exact exercise status |
|---|---|---|
| [Signal Processing Onramp](https://matlabacademy.mathworks.com/details/signal-processing-onramp/signalprocessing) | Orientation; loading and inspecting signal data; preparing and aligning recordings; frequency analysis; basic filtering; quantitative measurements; wrap-up. | All 40 graded tasks passed; 96% course indicator awaits the user's final survey. See the task-level progress record. |
| [Signal Generation and Resampling](https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr) | Orientation; synthesizing sampled waveforms; changing sampling rates; a square-wave application; wrap-up. | All 40 graded tasks passed after import recovery on 20 September; 6 code examples and 5 GUI activities verified. Personal survey unanswered; latest observed header 95%. |
| [Spectral Analysis Techniques](https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat) | Orientation; Fourier computation; basic PSD estimation; denser frequency sampling; leakage and windows; averaging noisy spectra; model-based and subspace estimators; wrap-up. | All 31 graded tasks passed, plus 5 code examples and 2 GUI activities. Conclusion reviewed; personal survey unanswered. Latest observed header 96%. |
| [Time-Frequency Analysis](https://matlabacademy.mathworks.com/details/time-frequency-analysis/otmltfa) | Orientation; changing signal frequencies; windowed Fourier methods; wavelet methods; a fan-fault application; wrap-up. | All 24 graded tasks passed and one ungraded window-length GUI activity verified. Conclusion reviewed; personal survey unanswered. Latest observed header 95%. |
| [Filter Design and Analysis Methods](https://matlabacademy.mathworks.com/details/filter-design-and-analysis-methods/otmlfdam) | Orientation; specification-driven designs; algorithm-driven designs; response and delay analysis; custom response shapes; pole/zero stability; wrap-up. | All 37 graded tasks passed, plus 10 code examples and 3 GUI activities. Conclusion reviewed; personal survey unanswered. Latest observed header 96%. |

This accounts for **33 public modules**, including introductory and concluding material. It is not a count of coding exercises. The machine-readable [inventory](course_inventory.json) records each module separately. Unknown completion states use `null`; all five started courses use `false` for full course completion. All five courses have completed graded work with personal surveys unanswered.

## Existing practice coverage

These mappings audit the original six files in `../coding_exercises/04_mathworks/`, before this package was revised. Links open their current copies in `practice/`; see the package README for subsequent fixes. Each is original supporting practice, not an export of the Academy tasks.

| Existing file | Implemented practice | Important gap |
|---|---|---|
| [onramp_signal_workflow.m](practice/onramp_signal_workflow.m) | CSV import, time base, interval selection, detrending, lowpass processing, Welch PSD, peak and amplitude statistics. | No implemented signal alignment or resampling in this file; Signal Analyzer appears only as an optional commented instruction. No earthquake course data. |
| [signal_generation_resampling.m](practice/signal_generation_resampling.m) | Tones, chirp, square wave, generated watermark, rational resampling, aliasing, zero insertion, and audio upsampling. | Generated signals replace course assets; no task-by-task match or grader verification. |
| [spectral_analysis_methods.m](practice/spectral_analysis_methods.m) | FFT amplitude, periodograms, windows, Welch estimates, Burg and MUSIC. | Synthetic tones replace course fan recordings; required task parameters and outputs are unknown. |
| [time_frequency_methods.m](practice/time_frequency_methods.m) | Two STFT window lengths and optional wavelet plots. | Generated transient replaces the fan-fault project; wavelet branch can be skipped if its toolbox is unavailable. |
| [filter_design_analysis.m](practice/filter_design_analysis.m) | FIR/IIR construction, specification-based design, responses, group delay, poles, arbitrary magnitude, and generated watermark recovery. | Filter Designer is only an optional commented instruction; the underwater course example is absent. |
| [wearable_preprocessing.m](practice/wearable_preprocessing.m) | Original physiological-signal practice with missing samples, resampling, windows, subject splits, and training-only scaling. | Research application, with no claim that it is a task from either linked resource. |

To claim completion of an Academy task, record its identity and a short topic summary, available inputs, submitted code or GUI actions, and the platform's result. Practice execution and public-outline coverage alone do not establish that completion.
