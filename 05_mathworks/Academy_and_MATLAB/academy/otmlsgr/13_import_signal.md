# Import a Signal: verified GUI tasks

[Course source](https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr). All three tasks received **Correct!** on **20 September 2026 (Australia/Sydney)**.

This is an early course lesson. Its filename reflects when its successful results were saved, after the later lessons.

To replay these steps, open the Academy lesson with its supplied `flute` workspace variable available in Signal Analyzer. This file records the GUI actions; it does not bundle the course audio or automatically recreate the GUI state.

| Task | Final action performed | Grader |
|---|---|---|
| 1 | Dragged `flute` into a fresh Signal Analyzer GUI and assigned a sample rate of 16000 Hz. | Correct! |
| 2 | Used the panner to select 0–7 seconds, extracted `flute_ROI`, renamed it `fluteShort`, displayed `fluteShort` with `flute`, and restored the full range using Fit to View. | Correct! |
| 3 | Enabled Spectrum for both `flute` and `fluteShort`. | Correct! |

Earlier attempts displayed the recording but failed the plot/sample-rate checks; a direct command workaround also errored. Those attempts are historical troubleshooting, not extra exercises. The successful fresh-GUI attempt resolved the graded gap.

For the optional follow-up, enabled data cursors, set the frequency view to 0-1000 Hz, and moved a cursor onto the peak. Its rounded readout showed 0.52 kHz, `fluteShort` -37.6 dB, and `flute` -37.7 dB. No sub-Hz precision is claimed. Play was invoked with only `fluteShort` displayed, and the final UI showed Play enabled and Stop disabled. The cursor/playback follow-up counts as one GUI activity. The agent did not hear or assess the audio. The course header was verified at 95%; no full course completion is claimed.


