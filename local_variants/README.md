# Reviewed local source variants (pending exercises)

These two alternatives preserve useful local correctness repairs that are absent
from the original 84-notebook source catalogue. They are **prepared source**, with
no saved training outputs, and add no exercise-completion credit. The original
course notebooks and previous evidence remain unchanged.

| Variant | Exact change | Existing evidence and limit |
|---|---|---|
| `04_fastai_part2/22_noise-pred_pair_return.ipynb` | Source cell 48 (zero-based 47) returns `(x0, xt)` rather than only `x0`, matching the following sampler's two-value unpack. The preceding equations/RNG stay unchanged. | A saved tiny CPU fixture checked the pair against the original local values, preserved RNG and reproduced the old failure. Full training has not been run. |
| `04_fastai_part2/30_lsun_diffusion-simple_numeric_shard_assertions.ipynb` | Source cell 16 (zero-based 15) retains the original numeric-shard selectors and checks 173,220 train + 19,811 validation images, 193,031 total, instead of incorrectly expecting all 303,125 archive images in that selected split. | Existing full archive/split metadata supports the assertion. Training, validation selectors, 15 epochs, models and samplers were not changed or executed by this preparation. |

## Integration and execution identity

Both notebooks keep their original course setup and persistence cells. They need
the repository's shared helpers, original prerequisites and datasets; they are
not standalone files. Their embedded setup still names the corresponding main
course notebook. They are not registered as separate entries in the original
84-entry batch launcher, and their edited source must not inherit a successful
record from the unmodified source. An isolated clone/explicit variant-identity
integration is required before promoting either file into an execution workflow.
The first Markdown cell retains the historical Colab/Drive setup text; the root
repository README explains the current GitHub clone bootstrap.

No environment, model weights, dataset archive, authentication material, local
release controller or old checkpoint-restoration framework is bundled here.

## Attribution and provenance

These are local AI-assisted adaptations of fast.ai course22p2 teaching notebooks.
Each notebook retains its pinned upstream source URL in its first Markdown cell.
Keep the existing Part 2 Apache-2.0 notice at `../04_fastai_part2/LICENSE` and the
repository `../SOURCES.md` with these adaptations. No replacement blanket licence
or claim of original student authorship is made.

`LOCAL_VARIANT_PROVENANCE.json` records original/variant/copy SHA256 values,
changed cells, prior limited validation and exact upstream source links. Both
staged notebooks are byte-exact copies of their reviewed variants; no privacy
substitutions were needed. No new training or expanded tests were run to stage them.
