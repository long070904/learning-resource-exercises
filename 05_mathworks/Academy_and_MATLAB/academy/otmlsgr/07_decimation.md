# Decimate signals in Signal Analyzer

[Course source](https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr). All three tasks in **Decimation of Signals** received **Correct!** in the hosted Academy app.

| Task | Action performed | Observed result |
|---|---|---|
| 1 | Duplicated `sig`, named the copy `sigdect`, applied Resample with sample factor **0.167**, then accepted and displayed it. | `sigdect` contained 2005 samples at 4008 Hz. |
| 2 | Imported the course-provided `sigfilt` from the workspace, assigned a 4000 Hz sample rate, and displayed its spectrum with `sigdect`; unchecked `sig`. | The official comparison check passed. |
| 3 | Exported `sigdect` to the MATLAB workspace. | The exported variable was a 2005×1 double array, and the check passed. |

The entered factor was **0.167**, which gives the observed 4008 Hz rate. It is an approximation to one sixth.

The `sigfilt` supplied to this GUI lesson was a **1×12001** workspace array. It should not be identified with the **2001-element** result produced by the earlier filtering/downsampling exercise; the course supplied a different preset workspace here.

For the optional GUI follow-up, imported `sigbad` and assigned 4000 Hz. Displayed one signal at a time and pressed the enabled Play control for original `sig` at 24000 Hz, `sigbad` at 4000 Hz, and `sigdect` at 4008 Hz. Each action was performed after the previous playback returned to idle. The final UI showed Play enabled and Stop disabled.

The playback steps count together as one ungraded GUI activity, without an additional code example. The AI-assisted check confirmed the controls and their state; it did not include listening or audio-quality analysis. The course header was observed at 62%.
