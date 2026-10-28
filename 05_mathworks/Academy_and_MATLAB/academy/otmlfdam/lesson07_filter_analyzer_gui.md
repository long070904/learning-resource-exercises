# Filter Analyzer App

One ungraded GUI activity in `filtanaly.mlx` was completed on 25 September 2026.

1. Run the provided setup to create `designedFIR` and `designedIIR`. Their original `designfilt` calls use `SampleRate=fs`. The IIR call in this lesson does **not** supply a `ScaleSOS` argument.
2. Enter `filterAnalyzer` and run the section. Academy reported completion with no outputs.
3. Choose **Import Filter → Filter Objects**, select both `designedFIR` and `designedIIR` (Shift+Down was used in the list), then **Import and Close**.
4. Verify both imported rows show **16 kHz** sampling. Select **Group Delay** for comparison. The screenshot showed a constant FIR delay of **212 samples** and nonconstant IIR delay with peaks around **2.2 and 2.5 kHz**.
5. Select **Phase** and verify both filters are displayed. Close the app after comparison.

Launching the app and importing the filters belong to this single GUI activity, without an additional graded pass or code example. [lesson07_filter_analyzer.m](lesson07_filter_analyzer.m) preserves the provided setup and launch command. It requires Signal Processing Toolbox and the unbundled `NoisyFlute.wav`; the standalone setup has not been run independently.
