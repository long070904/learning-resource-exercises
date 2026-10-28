# Measurement tasks and Live Editor settings

[Academy lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=6v1&lesson=2&section=1). All six graded tasks received **Correct!** in the hosted runtime. The actual code submissions are saved in [lesson14_signal_measurements.m](lesson14_signal_measurements.m).

Tasks 1–3 computed the spectrogram, summed power across frequency bins, and converted that sum to decibels. The app showed `p` as 1024×522, `f` as 1024×1, and `t` as 522×1.

For Task 4, inserted **Find Local Extrema** in the Tasks 4–5 section, chose `pwr` as input, retained `maxIndices` as the output name, and assigned `t` to the X-axis. For Task 5, selected maxima with a minimum prominence of 10. The maximum count was 522, minimum separation 0, and flat-region selection was centered. Both task checks passed.

Task 6 used `quakeSec = t(maxIndices);` and passed. The ungraded follow-up plotted the actual filtered recording with a 50 Hz time base and added vertical lines at those event times. The runtime reported completion with one output.

The plain `.m` record uses `maxIndices = islocalmax(pwr,MinProminence=10);`. Its output was checked against the actual live-task `maxIndices` with `assert(isequal(maxIndices,islocalmax(pwr,MinProminence=10)));`, which returned without error in the hosted command window. The GUI checks remain the evidence for Tasks 4–5; this additional assertion establishes that the saved code reproduces their index output on the course data.

The displayed event times, in seconds, were 115.33, 149.73, 184.13, 211.65, 235.73, 273.57, 388.81, 521.25, 572.85, 584.89, 624.45, 698.41, 713.89, and 825.69. These values reflect the displayed precision. The assertion checks the saved implementation; it adds no practice-exercise count.

Before this lesson, the header was observed at 80%; this is a historical observation. No 84% observation was inferred from these passes. See [current progress](../../ACADEMY_PROGRESS.md) for the later course record and completion status.
