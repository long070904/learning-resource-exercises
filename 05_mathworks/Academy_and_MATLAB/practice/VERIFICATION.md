# MATLAB practice verification

This folder contains copies of the six original MATLAB topic-practice functions in `coding_exercises/04_mathworks`. The original files and synthetic dataset are unchanged. These independent examples support practice; Academy completion is documented in the separate [course record](../ACADEMY_PROGRESS.md).

## Execution status

MATLAB R2024a is installed at `C:\Program Files\MATLAB\R2024a\bin\matlab.exe`. The first sandboxed batch startup failed while loading the settings plugin. An approved batch retry outside the sandbox reached MathWorks startup but returned:

```text
Unable to communicate with required MathWorks services (error 5201).
```

A fresh batch retry returned the same Error 5201, before MATLAB could run the environment probe or a practice function. Signal Processing Toolbox and optional Wavelet Toolbox licenses remain unverified. The error occurred during startup, before any exercise assertion could run.

The full offline evidence archive retains `verification/matlab_environment.log`, `verification/matlab_practice.log` and `verification/startup_attempts.json` for both attempts. All seven copied `.m` files match their original sources by SHA-256, recorded in `verification/copy_integrity.json`. These detailed verification files are not included in this code repository.

## Prepared checks

`verify_practice.m` runs all six functions with hidden figures, then checks meaningful outcomes:

- Time-region length, finite filtered values and nonnegative PSD.
- Resampling lengths, the expected 10 Hz alias, and unchanged audio duration.
- Detection of the 12.3 Hz tone and finite spectral estimates.
- Localization and detectability of the simulated transient.
- Filter stability, improved signal error, watermark recovery and specified stopband attenuation.
- Disjoint wearable subject splits and normalization fitted on training subjects only.

The checks are ready but have **not run successfully**. A successful run will write `verification/results.json`; the practice functions will save plots, arrays and measurement tables to `results/`.

In a working MATLAB session, open this `practice` folder and run:

```matlab
verify_practice
```

## Required next step

[MathWorks' official Error 5201 guidance](https://www.mathworks.com/matlabcentral/answers/1815395-why-do-i-receive-error-5201-unable-to-access-services-required-to-run-matlab) identifies a licensing issue. It suggests restarting MATLAB, then restarting the computer/MathWorks Service Host if needed, and contacting support if the problem persists. No network settings, licensing credentials or service installation were changed during this task.

These logs cover the local batch attempts. The hosted Academy environment later worked, with task results recorded in [ACADEMY_PROGRESS.md](../ACADEMY_PROGRESS.md). The local practice scripts still need a successful run in their own environment.
