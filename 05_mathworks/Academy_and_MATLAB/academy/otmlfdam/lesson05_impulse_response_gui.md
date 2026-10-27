# Impulse Response

Both tasks in `fluteimp.mlx` received **Correct!** on 25 September 2026.

1. Use `designedFIR` for the minimum-order FIR bandpass with edges 2100, 2200, 2500, and 2600 Hz at 16000 Hz sampling. Retain 80 dB first-stopband attenuation, 1 dB passband ripple, and 60 dB second-stopband attenuation. Select **Impulse Response** in the Design Filter task. Show Code exposed `freqz(designedFIR,[],fs)` and `impz(designedFIR,[],fs)`.
2. Use `designedIIR` for the corresponding minimum-order IIR bandpass with 60 dB attenuation in each stopband, 1 dB ripple, and `ScaleSOS=true`. Select **Impulse Response**. The generated call was `impz(designedIIR,[],fs)`.

[lesson05_impulse_response.m](lesson05_impulse_response.m) preserves the observed generated designs and calls, with separate figures as a standalone adaptation. It requires Signal Processing Toolbox and the unbundled `NoisyFlute.wav` for its course setup. The replay has not been independently executed.

The follow-up only discussed automatic selection of the IIR impulse-response length. It adds no code example or ungraded GUI activity; the two interactive operations are already counted as graded tasks.
