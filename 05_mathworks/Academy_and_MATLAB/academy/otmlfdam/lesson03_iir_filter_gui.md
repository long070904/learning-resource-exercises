# Design an IIR Filter

Both tasks in `flutefiltiir.mlx` received **Correct!** on 25 September 2026.

1. Set the Design Filter task to **Bandpass IIR**, with frequency units **Hz**, sample rate `fs`, and output **`designedFilter`**. The initial automatic output name `designedFilter2` was corrected to the required name.
2. Use a minimum-order design with edges **2100, 2200, 2500, and 2600 Hz**.

The observed Show Code output preserved in [lesson03_iir_filter.m](lesson03_iir_filter.m) uses 60 dB attenuation in both stopbands, 1 dB passband ripple, sample rate 16000 Hz, and `ScaleSOS=true`. The response is displayed with `freqz(designedFilter,[],fs)` before the course applies the filter and inspects its output spectrum.

The replay requires Signal Processing Toolbox and the unbundled course `NoisyFlute.wav`. The saved version uses separate figures and has not been run independently. Both GUI tasks are already included in the graded total.

The ungraded playback example ran `soundsc(yin,fs); pause(3.5); soundsc(yout,fs);`. Academy reported a completed section with no outputs, and Stop was disabled. This counts as one code activity. The AI-assisted check confirmed execution and playback controls; it did not assess listening quality.
