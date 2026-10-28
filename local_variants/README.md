# Local variants for two pending exercises

These two notebooks contain small corrections to pending fast.ai Part 2
exercises. They are prepared source files, with no saved training outputs and
no additional completion credit. The corresponding notebooks in the main
84-entry collection remain unchanged.

| Variant | Change | Validation and remaining work |
|---|---|---|
| [Noise-prediction pair return](04_fastai_part2/22_noise-pred_pair_return.ipynb) | Cell 48 (zero-based index 47) returns `(x0, xt)` instead of only `x0`, matching the sampler's two-value unpacking. The equations and random-number sequence are unchanged. | A small saved CPU check reproduced the original failure and checked the returned pair against the original local values. Full training has not run. |
| [LSUN numeric-shard assertions](04_fastai_part2/30_lsun_diffusion-simple_numeric_shard_assertions.ipynb) | Cell 16 (zero-based index 15) retains the numeric-shard selection and checks 173,220 training plus 19,811 validation images: 193,031 in total. The selected split does not contain all 303,125 archive images. | Existing archive and split metadata support the corrected assertion. The selectors, 15-epoch budget, models and samplers were not changed or executed during this preparation. |

## Running a variant

Both files retain the course setup and persistence cells, so they need the
repository's shared helpers, original datasets and other prerequisites. They
are not standalone notebooks. The historical setup cells still name the
corresponding main course notebook, and neither variant is registered as a
separate exercise in the batch launcher.

Before running either variant, give it a separate execution identity and result
location. A result from the unchanged main notebook must not be reused as proof
that the edited variant ran. The [repository README](../README.md) explains the
GitHub clone setup; the first Markdown cell in each variant retains the earlier
Colab/Drive instructions.

## Sources and file history

These are AI-assisted local adaptations of fast.ai course22p2 notebooks. Their
first Markdown cells retain the pinned upstream source URLs. Keep the existing
[Part 2 Apache-2.0 licence](../04_fastai_part2/LICENSE) and
[source credits](../SOURCES.md) with the files.

[LOCAL_VARIANT_PROVENANCE.json](LOCAL_VARIANT_PROVENANCE.json) records the original,
variant and repository-copy hashes, changed cells, upstream links and limited
validation. The repository copies match the reviewed variants byte for byte;
no privacy substitutions were needed. No new training or broader tests were
run when these files were added. Datasets, model weights, credentials and the
local checkpoint-restoration tools are not included.
