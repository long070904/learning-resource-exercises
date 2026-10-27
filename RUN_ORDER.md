# Run order and required data

## Google

Run 01–04 individually. Run `05_fairness_income_colab` in a fresh runtime; it installs matching TensorFlow/tf-keras and uses the actual MinDiff wrapper. `05b` is the separate PyTorch MMD adaptation. `06` is the synthetic wearable subject-split application.

## MIT

Lab 1: run 01 then 02 in either PyTorch or TensorFlow. Both versions are supplied; each music notebook can prepare its own vocabulary and model. The wearable applications 03–04 are additional practice.

Lab 2: 05 covers MNIST, 06 covers facial detection/debiasing; choose PyTorch or TensorFlow. The face-data notebook downloads the official large teaching dataset and requires a GPU. It does not perform face identification. Lab 3: 07 covers tokenization, generation, LoRA fine-tuning, and the documented local judge/tracing adaptation. The official API judging and Opik UI exercises require the separate 08 service continuation, an OpenRouter account, an Opik account, and Colab Secrets named OPENROUTER_API_KEY and OPIK_API_KEY. A source-permitted free OpenRouter judge is available; it has request limits. Service calls remain disabled until explicitly authorized. Local Qwen scores and JSON traces do not establish completion of those official service exercises.

## fast.ai Part 1

Run image notebook 00 before 02 or 03. Use the same QUICK_RUN value so the image folders match. Keep Drive enabled to preserve the exported learner across sessions. In a new session, rerun 00 to recreate the local images before 02/03. Notebooks 04–09 are independent.

Notebooks 10–13 are Road to the Top parts 1–4. Accept the competition rules and download [Paddy Disease Classification](https://www.kaggle.com/competitions/paddy-disease-classification/data), then put `paddy-disease-classification.zip` at the top of My Drive or upload when prompted. These are the real competition exercises; no synthetic data is silently substituted. Batch sizes are smaller than the originals for Colab GPUs. In notebook 12, the original large-model comparisons and ensemble can still require more memory/time than a free T4 runtime.

Notebook 14 is the original Lesson 4 NLP exercise. Similarly provide `us-patent-phrase-to-phrase-matching.zip` from [Kaggle](https://www.kaggle.com/competitions/us-patent-phrase-to-phrase-matching/data). Notebooks 15 and 16 download MovieLens and MNIST automatically. These correspond to collaborative filtering and convolutions. Their QUICK_RUN option uses smaller real-data samples and one epoch per model. Deployment account setup and ethics discussions are learner activities.

Notebooks 17–24 add the full official course22 clean notebooks 00–07. They preserve all 257 upstream cells and 201 nonempty code cells, including Oxford Pets training/export, the historical timm benchmark analysis, manual neural-network experiments, complete Titanic feature/model comparisons, the five-model 16-epoch ensemble, and the original manual/random-forest experiments. Existing 00–07 are shorter companion exercises and remain separately identified. The new Titanic notebooks use verified public copies of the original 891 training and 418 test rows, preserve the original features, and save predictions without submitting them. Run 17–24 in numerical order; the remaining full Part 1 exercises are 08–16.

## fast.ai Part 2

Begin with `diffusion_intro/01`, `02`, and `03` for Lessons 9–10, then work through numbered notebooks 01–31 in the main Part 2 folder. The supplied `miniai` package makes notebook imports independent of running nbdev exports. The filenames retain upstream numbering, including variants 16A/16B, 22, 24, and 30. Experimental underscore-prefixed repository scratch notebooks are not course exercises and are not included.

Use a GPU for this original course code. Heavy image runs use batches of 8 and smaller Fashion MNIST runs use 32; these change batch conditions while preserving the original training durations. Full diffusion/ImageNet runs can take multiple sessions. QUICK_RUN does not shorten these notebooks.

| Before opening | Complete first | Files needed in the persistent models folder |
|---|---|---|
| 18_fid | 14_augment and 17_DDPM_v2 | data_aug2.pkl; fashion_ddpm_mp.pkl |
| 19_DDPM_v3 | 14_augment | data_aug2.pkl |
| 20_DDIM | 14_augment and 19_DDPM_v3 | data_aug2.pkl; fashion_ddpm3_25.pkl |
| 22 variants, 23, 26, 28 | 14_augment | data_aug2.pkl |
| 25_superres | 24_imgnet_tiny | inettiny-custom-25; local Tiny ImageNet data |

The notebook setup reports missing checkpoints before starting long training. Keep Drive enabled so checkpoints are available in the next runtime. Whole-model pickle checkpoints must be your own trusted outputs; they contain executable Python object definitions.

Notebook 31 is the full ImageNet latent experiment. Its local route needs original CLS-LOC images at `data/ILSVRC/Data/CLS-LOC`, plus `imagenet_lsvrc_2015_synsets.txt` and `words.txt` in `data/ILSVRC`. An optional official Hugging Face streaming route requires approved dataset access, a scoped HF_TOKEN, and the same original synset metadata. It pins the dataset revision and refuses an unverified label mapping. The full 1,281,167 training and 50,000 validation examples remain required. Streaming avoids retaining every raw image; the original float32 latent cache still needs approximately 27.26 GB on runtime disk. Only manifests, checkpoints, and results persist to Drive. Tiny ImageNet and LSUN notebooks download their public course archives, verify complete inputs, and require substantial runtime disk. Runtime inputs disappear when the runtime is deleted.

## Coverage limits

This edition covers the current MIT labs 1–3, the Part 1 code exercises and companions listed in the index, all numbered course22p2 notebooks, and diffusion-nbs notebook exercises. Archived MIT extra labs and every book chapter are not silently included under the label of current course exercises. Quizzes and interactive Google widgets are linked from the official exercise inventory; they do not become Python notebooks. Full-model training and private/account-controlled data paths cannot be verified without the corresponding runtime and inputs.
