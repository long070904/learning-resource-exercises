# MIT Introduction to Deep Learning

The selected MIT 6.S191 labs are kept alongside two wearable modelling
companions. Eleven of the twelve notebooks have saved runs in the
25 October 2026 review. The separate service continuation is still pending.

| Work | Notebooks |
|---|---|
| Lab 1: tensors and gradients | [PyTorch](01_pt_tensor_and_gradient_exercises.ipynb), [TensorFlow](01_tf_tensor_and_gradient_exercises.ipynb) |
| Lab 1: music generation | [PyTorch](02_pt_music_generation.ipynb), [TensorFlow](02_tf_music_generation.ipynb) |
| Wearable recurrent models | [LSTM, GRU and temporal attention](03_wearable_lstm_gru_attention.ipynb) |
| Wearable Transformer | [Contrastive learning and a frozen probe](04_transformer_contrastive_prototype.ipynb) |
| Lab 2: MNIST | [PyTorch](05_pt_lab2_mnist.ipynb), [TensorFlow](05_tf_lab2_mnist.ipynb) |
| Lab 2: detection and debiasing | [PyTorch](06_pt_lab2_debiasing.ipynb), [TensorFlow](06_tf_lab2_debiasing.ipynb) |
| Lab 3: language-model fine-tuning | [Fine-tuning notebook](07_lab3_llm_finetuning.ipynb) |
| Lab 3: external services | [Continuation notebook](08_lab3_service_continuation.ipynb) and [setup notes](08_lab3_service_continuation_README.md) |

The [work index](../WORK_INDEX.md#mit-6s191) links the saved notebooks.
Generated music is in [results/audio](../results/audio). Use a fresh environment
when switching frameworks; the [run guide](../RUN_ORDER.md#mit-6s191) lists the
larger data requirements.

The wearable companions use synthetic signals. Temporal attention and
missing-channel tests are practice examples, rather than a replication of a
published wearable model. Local judge scores and trace files from Lab 3 are
also separate from the OpenRouter and Opik service tasks.

Original teaching material is from
[MIT 6.S191](https://github.com/MITDeepLearning/introtodeeplearning).
The [source index](../EXERCISE_INDEX.md) records revisions and AI-assisted adaptations.
