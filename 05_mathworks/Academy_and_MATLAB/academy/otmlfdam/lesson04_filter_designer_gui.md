# Design a Filter Using Filter Designer

One ungraded GUI workflow was completed on 25 September 2026. The design, export and integrated filtering steps count together as one GUI activity, without an additional graded pass or code example.

1. Launch `filterDesigner`. Select **Bandpass FIR**, design by **Algorithm**, method **Window**, and a **Rectangular** window.
2. Set sample rate to **16000 Hz**, specify **order 200**, and set the **6 dB cutoff frequencies to 2200 Hz and 2500 Hz**. The exercise allowed the order to be chosen; 200 was the value used.
3. Select **Update Filter**, then export **Coefficients** to the **MATLAB Workspace**. Confirm export and close Filter Designer.
4. The workspace contained `bandpassfir1_Num` as a **1×201 double**. Run `yout=filter(bandpassfir1_Num,1,marked); pwelch(yout,[],[],[],fs);`. The Command Window prompt returned.

The exported coefficients were checked against this reconstruction in the hosted runtime:

```matlab
bReplay=fir1(200,[2200 2500]/(fs/2),rectwin(201));
max(abs(bReplay-bandpassfir1_Num))
```

The result was **0**, establishing an exact match for the observed export in that session. [lesson04_filter_designer.m](lesson04_filter_designer.m) uses that reconstruction, with the original signal setup and integrated filtering calculation. It requires Signal Processing Toolbox and the unbundled course `NoisyFlute.wav`. The complete standalone version, including its separate figures, has not been run independently.
