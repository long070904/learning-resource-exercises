# Interactively Design a Filter

Verified in the signed-in Filter Design and Analysis Methods course on 25 September 2026. The lesson used `flutesetuptask.mlx` and the real course `NoisyFlute.wav`, which is not bundled.

1. Insert the **Design Filter** Live Editor task, select **Bandpass FIR**, and retain its default specifications. Use output variable `designedFilter`. The task received **Correct!**.
2. Run `yout=filter(designedFilter,marked);`. The task received **Correct!**.
3. Run `pwelch(yout,[],[],[],fs);`. The task received **Correct!**.

The task's Show Code view exposed the `designfilt` call preserved in [lesson01_design_filter.m](lesson01_design_filter.m). Its normalized edges are 0.35, 0.45, 0.55, and 0.65, with 60 dB stopband attenuation on each side and 1 dB passband ripple. The code also calls `freqz(designedFilter)`.

The `.m` file combines the generated design and accepted calculations in separate figures. This standalone version has not been run independently. The interactive design belongs to the three graded tasks; the conceptual follow-up and optional repeat of the same code add no ungraded activities.
