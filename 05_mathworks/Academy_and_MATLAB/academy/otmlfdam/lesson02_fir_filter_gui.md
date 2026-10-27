# Design an FIR Filter

The `flutefiltpassstop.mlx` lesson's three tasks received **Correct!** on 25 September 2026:

1. Set the Design Filter task to use **Hz**, with sample rate `fs`.
2. Use a minimum-order bandpass FIR design with stopband/passband edges **2100, 2200, 2500, and 2600 Hz**.
3. Increase the lower-stopband attenuation to **80 dB**, retaining **1 dB** passband ripple and **60 dB** upper-stopband attenuation.

The Show Code view generated the design in [lesson02_fir_filter.m](lesson02_fir_filter.m), including `SampleRate=16000`. The generated task also called `freqz(designedFilter,[],fs)` and `info(designedFilter)`.

For one ungraded GUI comparison, Filter Information was selected. The 80 dB setting showed **length 425**. Changing only the lower-stopband attenuation to 60 dB showed **length 317**. Restoring 80 dB restored length 425. Thus the stronger attenuation added 108 coefficients; the corresponding orders are 424 and 316. The final task setting remains 80 dB.

For one separate ungraded code example, the playback lines `soundsc(yin,fs); pause(3.5); soundsc(yout,fs);` were uncommented and run. Academy reported a completed section with no outputs. The commands executed, but no listening or subjective quality comparison is claimed.

The replay requires Signal Processing Toolbox and the course `NoisyFlute.wav`, which is not bundled. Its standalone arrangement has not been independently executed.
