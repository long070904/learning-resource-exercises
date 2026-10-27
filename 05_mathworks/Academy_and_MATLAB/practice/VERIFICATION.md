# MATLAB practice verification

These are copies of the six original MATLAB topic-practice functions in `coding_exercises/04_mathworks`. The original files and synthetic dataset remain unchanged. They are **not** the authenticated MathWorks Academy exercises or evidence of course completion.

## Execution status

MATLAB R2024a is installed at `C:\Program Files\MATLAB\R2024a\bin\matlab.exe`. The first sandboxed batch startup failed while loading the settings plugin. An approved batch retry outside the sandbox reached MathWorks startup but returned:

```text
Unable to communicate with required MathWorks services (error 5201).
```

One fresh batch retry returned the same Error 5201. MATLAB did not execute the environment probe or any practice function. The Signal Processing Toolbox and optional Wavelet Toolbox licenses therefore remain unverified. The startup failure is not a failed exercise assertion.

The original MATLAB log is preserved at [verification/matlab_environment.log](verification/matlab_environment.log). The fresh batch retry is recorded separately at [verification/matlab_practice.log](verification/matlab_practice.log). The machine-readable attempt record is [verification/startup_attempts.json](verification/startup_attempts.json). SHA-256 comparison confirmed that all seven copied `.m` files match their original sources; see [verification/copy_integrity.json](verification/copy_integrity.json).

## Prepared checks

`verify_practice.m` runs all six functions with hidden figures, then checks meaningful outcomes:

- Time-region length, finite filtered values and nonnegative PSD.
- Resampling lengths, the expected 10 Hz alias, and unchanged audio duration.
- Detection of the 12.3 Hz tone and finite spectral estimates.
- Localization and detectability of the simulated transient.
- Filter stability, improved signal error, watermark recovery and specified stopband attenuation.
- Disjoint wearable subject splits and normalization fitted on training subjects only.

These checks have been prepared but have **not run successfully**. When they run, they write `verification/results.json`, and the practice functions write plots, arrays and measurement tables to `results/`.

In a working MATLAB session, open this `practice` folder and run:

```matlab
verify_practice
```

## Required next step

[MathWorks' official Error 5201 guidance](https://www.mathworks.com/matlabcentral/answers/1815395-why-do-i-receive-error-5201-unable-to-access-services-required-to-run-matlab) identifies a licensing issue. It suggests restarting MATLAB, then restarting the computer/MathWorks Service Host if needed, and contacting support if the problem persists. No network settings, licensing credentials or service installation were changed during this task.

This record covers the earlier local batch attempts only. The authenticated hosted Academy runtime subsequently worked and has verified task results recorded in [ACADEMY_PROGRESS.md](../ACADEMY_PROGRESS.md). Those hosted results do not imply that these independent local practice scripts have run successfully.
