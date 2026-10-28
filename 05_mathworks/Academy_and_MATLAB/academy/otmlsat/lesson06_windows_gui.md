# Create and apply windows

[Course source](https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat). All five tasks received **Correct!** on 20 September 2026.

The course startup loaded `psdsig`, formed `sig=1e-3*sin(2*pi*fr*t);`, and set `n=length(sig);`. Its data file remains an external course asset.

| Task | Actual action in the hosted runtime | Grader |
|---|---|---|
| 1 | Launched `windowDesigner`; named the window `w`, selected Rectangular, set length 2400, applied it, and saved it to the workspace. Ran the course plot of `w` against `t`. | Correct! |
| 2 | Ran `periodogram(sig,w,2^12,fs);`. | Correct! |
| 3 | Replaced `w` with Hamming, length 2400, using Apply and Save in Window Designer. | Correct! |
| 4 | Replaced `w` with Kaiser, length 2400 and beta 1, using Apply and Save. | Correct! |
| 5 | Changed the Kaiser beta to 20, applied it, and saved the resulting `w`. | Correct! |

[lesson06_windows.m](lesson06_windows.m) is a code-based replay of these settings using `ones`, `hamming`, and `kaiser`. It was not separately executed or compared sample-for-sample with the actual GUI exports. The table records the settings checked by the Academy grader.

The provided `compwindows.mlx` ran as an ungraded example and completed with two outputs. [compwindows.m](compwindows.m) preserves its computations and labels, adding separate figures for standalone display. The windowing summary and background pages were reviewed; the videos were not played. The latest observed course header was 46%.
