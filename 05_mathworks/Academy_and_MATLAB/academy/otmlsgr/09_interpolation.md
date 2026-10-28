# Interpolate signals in Signal Analyzer

[Course source](https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr). All three tasks in **Interpolation of Signals** received **Correct!** in the hosted Academy app.

| Task | Action performed | Observed result |
|---|---|---|
| 1 | Duplicated `sig` as `sigint`, applied Resample with sample factor **6**, then accepted and displayed it. | 9006 samples at 18000 Hz. |
| 2 | Imported the provided 9006-sample `sigfilt` from the workspace, assigned a sample rate of 18000 Hz, and displayed its spectrum with `sigint`; unchecked `sig`. | The official comparison check passed. |
| 3 | Exported `sigint` to the MATLAB workspace. | The exported variable was a 9006×1 double array, and the check passed. |

For the optional follow-up, imported `sigbad` and assigned 18000 Hz. Displayed one signal at a time and invoked the enabled Play control for original `sig` at 3000 Hz, `sigbad` at 18000 Hz, and `sigint` at 18000 Hz. The final UI showed Play enabled and Stop disabled.

The playback steps count together as one ungraded GUI activity, without an additional code example. The AI-assisted check covered the controls; listening quality was not assessed. The course header was observed at 70%.
