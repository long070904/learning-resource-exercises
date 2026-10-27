These prepared notebooks require hosted execution before any training task is recorded as finished. Local validation checked syntax, loss masking, model shapes, batch normalization, HDF5 streaming and corpus batches only; it did not train models or produce course completion.

Use one notebook kernel/process at a time, QUICK_RUN=False, and a GPU runtime. Keep the shared colab_runtime.py setup. The current observed Colab allocation is a T4 with approximately 15 GB GPU memory and 12.7 GB system RAM. Use fresh kernels when moving between frameworks/profiles. PyTorch and TensorFlow GPU allocations must not overlap between notebook processes.

Run the nine original-course notebooks in this order:

1. 01_pt_tensor_and_gradient_exercises.ipynb
2. 01_tf_tensor_and_gradient_exercises.ipynb
3. 02_pt_music_generation.ipynb
4. 02_tf_music_generation.ipynb
5. 05_pt_lab2_mnist.ipynb
6. 05_tf_lab2_mnist.ipynb
7. 06_pt_lab2_debiasing.ipynb
8. 06_tf_lab2_debiasing.ipynb
9. 07_lab3_llm_finetuning.ipynb

The two wearable/contrastive notebooks are separate synthetic practice prototypes, not MIT Labs 2–3 or finished real research implementations. Do not count them as original course exercise completion.

Dependency notes:

- Preserve Colab's working torch/torchvision/CUDA combination. The shared mit profile adds mitdeeplearning==0.7.5, torchsummary, h5py and OpenCV. mitdeeplearning imports TensorFlow even in PyTorch notebooks, so TensorFlow must also be importable. Avoid letting it allocate GPU memory during PyTorch runs.
- Python 3.13 is supported by TensorFlow 2.21.0's Linux cp313 wheels and current PyTorch wheels. The shared TensorFlow range permits 2.21. Colab's actual installed CUDA packages still need a GPU import/probe. Official source: https://www.tensorflow.org/install/pip and https://pypi.org/project/tensorflow/2.21.0/ . Do not downgrade Python solely on the assumption TensorFlow lacks cp313 wheels.
- Music uses Debian abcmidi, timidity, and fluid-soundfont-gm. The notebook installs them in Colab if absent. It must render a nonempty WAV from generated ABC, display audio, and retain ABC/MIDI/WAV files. Internet and package installation are needed; unsuccessful conversion prevents completion.
- MNIST uses the full original 60,000/10,000 split. Optimizer/learning-rate comparisons use 54,000 training and 6,000 validation examples for two epochs per candidate; selected models are then freshly trained on all 60,000 examples for the original final budget (FC five epochs; CNN seven PyTorch/five TensorFlow). TensorFlow also completes the explicit GradientTape full epoch with batch size 12. Final test data is excluded from optimizer selection.
- Debiasing downloads the official CelebA/ImageNet HDF5 teaching dataset via the course's Dropbox link. It needs several GB of download/disk space. The loader now streams uint8 images and converts batches to float32. Adaptive sampling considers every positive face via small latent chunks. Both classifier and DB-VAE use the entire source dataset and two nominal epochs of balanced stochastic sampling, with N//32 steps per epoch. This is the original sampling scheme, not a guarantee every individual example is visited. There is no synthetic fallback. Dataset download/schema failures stop the exercise.
- Lab 3 uses original public LiquidAI/LFM2-1.2B and course Dolly/style data. Use transformers>=4.55,<5, peft>=0.17,<1, accelerate>=1,<2, datasets>=3,<5, lion-pytorch, mitdeeplearning==0.7.5. No mandatory Hugging Face token is needed for these public models. LFM2 optional accelerated convolution kernels are not required and should not be built merely for a compatibility check. The frozen base is float16; rank-8 LoRA parameters and loss are float32, context 512, gradient checkpointing, batch size one, Lion learning rate 1e-4. Each style has exactly 200 successful optimizer updates. Leprechaun and Yoda start from independent original base weights.
- Default Lab 3 judge is public Qwen/Qwen2.5-3B-Instruct, larger than the performer, loaded in float16 on the T4. Its roughly 6 GB GPU weights coexist with the roughly 2.4 GB performer; inference context is bounded to 1,536 tokens. The judge is released after monitoring and before checkpoint restoration. The hosted runner must catch an actual memory failure and preserve outputs if the allocation is smaller; do not silently replace it with a smaller judge or skip the evaluation.
- Lab 3 local JSON traces are an explicit adaptation of hosted Opik, and Qwen scores are an explicit adaptation of Gemini/OpenRouter. Gemini scores are not inferred or fabricated. Exact hosted service steps require the user's own OpenRouter account/key/credits and Opik/Comet account/key. Default RUN_HOSTED_JUDGE=False and RUN_OPIK_REMOTE=False. No paid API calls are made by default. The final record marks official_service_exercises_completed false unless both service modes run. No competition submission is made.

Completion evidence:

Each original notebook writes a unique results/<notebook>/<UTC-run-id>/task_evidence.json and model artifacts. Required checks must exist before finish_run writes the final record; runtime versions and Colab provenance are recorded. Merely reaching an empty final cell, having filled solution code, downloading a file, passing the local light checks, or producing synthetic prototype results is insufficient. Preserve the executed .ipynb outputs and errors independently of the result JSON.

Sources for exercise scope and adaptations:

- MIT official labs: https://github.com/MITDeepLearning/introtodeeplearning
- Music exercise: https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab1/PT_Part2_Music_Generation.ipynb
- Original HDF5 loader/test groups: https://github.com/MITDeepLearning/introtodeeplearning/blob/master/mitdeeplearning/lab2.py
- Original Dolly/style loader: https://github.com/MITDeepLearning/introtodeeplearning/blob/master/mitdeeplearning/lab3.py
- Lab 3: https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab3/LLM_Finetuning.ipynb
- Performer card: https://huggingface.co/LiquidAI/LFM2-1.2B
- Adapted local judge card: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- Chat template guidance: https://huggingface.co/docs/transformers/chat_templating
- Opik metric interface: https://www.comet.com/docs/opik/python-sdk-reference/evaluation/metrics/BaseMetric.html
