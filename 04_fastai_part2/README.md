# fast.ai Part 2

Forty notebooks cover foundations and diffusion, including three introductions
in `diffusion_intro`. The 25 October 2026 review records 22 saved runs and
18 pending exercises. The [work index](../WORK_INDEX.md#fastai-part-2) links each
source and available output.

## Finding a notebook

Begin with the three diffusion introductions, then follow the numbered
notebooks. Original filenames are retained, including 16A/16B and the variants
of 22, 24 and 30. The bundled `miniai` modules support course imports without
rerunning nbdev exports.

Later exercises depend on models saved by earlier notebooks. Read the
[checkpoint table](../RUN_ORDER.md#fastai-part-2) before a long run. GPU memory,
runtime disk space and dataset access matter particularly for ImageNet, LSUN
and latent-diffusion work.

## Reading saved results

Notebook 15 retains its validation-curve error after training and sampling.
A separate audit checked the saved artifacts without additional training;
both records are included. Notebook 17 has its own saved execution and is a
separate exercise. The [results guide](../results/README.md) explains these
records and the remaining work.

The [local variants](../local_variants/README.md) contain two reviewed source
fixes for pending exercises. Those fixes have not established successful full runs.

Original material comes from [course22p2](https://github.com/fastai/course22p2)
and [diffusion-nbs](https://github.com/fastai/diffusion-nbs).
The [source index](../EXERCISE_INDEX.md) records revisions and adaptations,
including AI-assisted setup work. Original course notices remain with the
notebooks and exported modules.
