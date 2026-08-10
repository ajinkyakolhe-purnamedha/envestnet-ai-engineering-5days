# Offline Hugging Face model bundle

This repository is structured so every committed file stays below GitHub's strict 100 MB file limit.

Included models:

- `BAAI/bge-small-en-v1.5`, quantized ONNX embedding model.
- `HuggingFaceTB/SmolLM2-135M-Instruct`, sharded `safetensors` generative model for `transformers`.

For BGE, a sharded Transformers `safetensors` copy is also possible, but it is larger than the quantized ONNX bundle. The current ONNX layout already gives the same GitHub-safe property because the model is split into `model_quantized.onnx` and `model_quantized.onnx_data`, both under 100 MB.

The SmolLM2 weights are stored as standard Transformers sharded safetensors under:

```text
models/smollm2-135m-instruct/
```

Transformers loads the shards automatically from `model.safetensors.index.json`.

Run the offline recipe notebook:

```bash
jupyter notebook offline_hf_hub_offline_demo.ipynb
```

GitHub upload status:

- The model weights can be committed to a normal GitHub repository without Git LFS because every individual file is under 100 MB.
- The largest files are the SmolLM2 shards, each under 90 MB.
- Participants can clone the repository and run the notebook without connecting to Hugging Face, assuming Python dependencies are already installed.
