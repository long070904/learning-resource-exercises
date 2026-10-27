# Apply lowpass filtering in Signal Analyzer

[Academy lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=5v1&lesson=2&section=1). All three GUI tasks received **Correct!** in the hosted Academy app.

| Task | Action performed | Grader |
|---|---|---|
| 1 | Copied `wanc` to `wanc_filt`. Applied Lowpass with passband 0.1 Hz, default steepness 0.85, and stopband attenuation 60 dB. Accepted the change and displayed both spectra. | Correct! |
| 2 | Displayed `harp`, `pax`, and `wanc_filt` in time and spectrum views. | Correct! |
| 3 | Copied the original `wanc` to `wanc_steep`. Applied Lowpass at 0.1 Hz with steepness 0.95, then displayed `harp`, `pax`, and `wanc_steep` in time and spectrum views. | Correct! |

For further practice, ran [steepness_comparison.m](steepness_comparison.m)'s commands in the hosted MATLAB command window. The comparison used steepness values 0.5 and 0.99 at a 50 Hz sample rate. Execution returned to the command prompt without errors, `soft` and `sharp` were each 45107×1, and a Figure 1 tab was created.

The resulting figure graphic was obscured by the Signal Analyzer overlay. Its creation was observed, but its plotted curves were not visually inspected. This was an ungraded code run, separate from the three verified GUI tasks.

The course header was observed at 72%. The script requires the real course `wanc` array to be loaded in the workspace; that data is not bundled here.
