# Apply and compare bandpass filtering

[Academy lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=5v1&lesson=3&section=1). Both GUI tasks received **Correct!** in the hosted Academy app.

| Task | Action performed | Grader |
|---|---|---|
| 1 | Copied `wanc` to `wanc_bandpass`. Applied Bandpass from 2 to 10 Hz with default steepness 0.85 and stopband attenuation 60 dB. Accepted the result and displayed the original and filtered recordings in time and spectrum views. | Correct! |
| 2 | Displayed `wanc_lowpass` with `wanc_bandpass`, enabled the panner, and set time limits to 180–300 seconds (3–5 minutes). | Correct! |

Optional time-axis amplitude limits of −0.2 to 0.2 were also applied. For the ungraded follow-up, displayed `harp` with `wanc_bandpass` over 3-5 minutes, kept the panner enabled, and unchecked `wanc_lowpass`. A screenshot confirmed the slow harp wave and bandpass pulses. Adding `harp` autoscaled the amplitude axis; the earlier -0.2 to 0.2 limits did not persist. This counts as a performed GUI follow-up, without another graded pass.

The course header was observed at 76%. The names and actions above refer to the actual hosted course workspace.

