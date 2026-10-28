# Resample recordings in Signal Analyzer

[Academy lesson](https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=2&section=1). Each of the three app tasks received **Correct!** in the hosted runtime.

| Task | Action performed | Grader |
|---|---|---|
| 1 | Duplicated `pax` as `pax_uniform`. In Resample, chose a 50 Hz sample rate with the default linear interpolation, then Apply → OK → Accept All. Displayed `pax` with `pax_uniform`. | Correct! |
| 2 | Displayed `wanc` alone, including its full power spectrum from 0 to 50 Hz. | Correct! |
| 3 | Duplicated `wanc` as `wanc_slow`. In Resample, chose sample-factor mode with a factor of 0.5, then Apply → OK → Accept All. Displayed `wanc` with `wanc_slow`. | Correct! |

The app reported `wanc_slow` as **126000 samples at 50 Hz**. For the ungraded follow-up, all five signals were selected and both time and power-spectrum views were visible. The spectra for `wanc_slow`, `harp`, and `pax_uniform` ended at 25 Hz; original `wanc` extended to 50 Hz. These limits correspond to half of their respective uniform sampling rates.

The follow-up counts as one ungraded GUI comparison. The header was observed at 36%. All actions used the course workspace in the hosted Academy runtime.
