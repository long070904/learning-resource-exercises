# Compare recordings in Signal Analyzer

[Academy lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=2v1&lesson=5&section=1). Each of the three GUI tasks received **Correct!** in the hosted Academy app.

| Task | Action performed | Grader |
|---|---|---|
| 1 | Selected `pax` in the signal table. In Analyzer → Time Values, chose the explicit time-vector mode and supplied `paxT`; enabled the `pax` checkbox. | Correct! |
| 2 | Selected `wanc`, assigned a 100 Hz sample rate with a 0-second start, and enabled its checkbox. | Correct! |
| 3 | Kept all three signals visible, enabled the spectrum display, and limited frequency to 0–1 Hz. | Correct! |

Using `paxT` retained the recording's irregular sample times. The app displayed `*Fs:50.0000Hz`; that display does not mean the explicit time vector was replaced with a uniform grid.

The further-practice explanatory notes were reviewed. They requested no additional operation, so no extra execution or grader result is claimed. The course header was observed at 28%. Course workspace data were used inside the hosted runtime.
