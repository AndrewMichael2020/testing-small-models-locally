# Gemma Runtime Smoke-Test Harness

This directory contains a Jupyter notebook for testing Google Gemma models across multiple runtimes.

## Notebook: `gemma_runtime_smoketest.ipynb`

A comprehensive testing harness that validates Gemma model runnability across:
- **Transformers** (Hugging Face)
- **Ollama** (external runtime)
- **llamafile** (single-file distribution)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Optional: Install Ollama

If you want to test the Ollama runtime:
- Download from [ollama.ai](https://ollama.ai)
- Start the Ollama server: `ollama serve`

### 3. Run the Notebook

```bash
jupyter notebook gemma_runtime_smoketest.ipynb
```

Or use VS Code with the Jupyter extension.

### 4. Provide Tokens

When prompted:
- **HF_TOKEN**: Your Hugging Face token (for accessing gated models)
- **OPENAI_API_KEY**: Your OpenAI API key (for report generation)

You can skip either token if you don't want to run those specific tests.

## Configuration

All configuration options are in the "Configuration Section" near the top of the notebook:

- **Runtime flags**: Enable/disable specific runtimes
- **Model lists**: Customize which models to test
- **Timeouts**: Adjust timeout values for different operations
- **Generation parameters**: Control max tokens, temperature, seed
- **Prompts**: Define test prompts (short and complex)
- **OpenAI model**: Choose which OpenAI model to use for report generation

## Output

The notebook produces several output files in the `artifacts/` directory:

- `results.jsonl`: Raw test results (one JSON object per line)
- `results.csv`: Flattened summary table
- `report.md`: Human-readable analysis from OpenAI
- `report.json`: Machine-readable report metadata

## What Gets Tested

For each model and runtime combination, the notebook:

1. Downloads/pulls the model (with timeout)
2. Loads it into memory
3. Runs inference on two prompts:
   - Short sanity check
   - Complex JSON extraction task
4. Records timing and success/failure status
5. Clears memory before moving to the next test

## Expected Behavior

### Success
- Model loads and generates output
- Timings are recorded
- Output is captured
- Status: `SUCCESS`

### Failure
- Model fails to download (gating, network issues)
- Out of memory
- Inference timeout
- Runtime not installed
- Status: `FAILED` with error details

### Skipped
- Runtime not available
- Token not provided for gated models
- Status: `SKIPPED` with reason

## Tested Models

### Gemma 3 (Primary)
- `google/gemma-3-1b-it` (Transformers)
- `google/gemma-3-4b-it` (Transformers)
- `google/gemma-3-12b-it` (Transformers)
- `gemma3:1b`, `gemma3:4b`, `gemma3:12b` (Ollama)
- `mozilla-ai/gemma-3-*-llamafile` (llamafile)

### Gemma 2 (Fallback)
- `google/gemma-2-2b-it`, `google/gemma-2-9b-it` (Transformers)
- `gemma2:2b`, `gemma2:9b` (Ollama)
- `mozilla-ai/gemma-2-2b-it-llamafile` (llamafile)

## Troubleshooting

### "Ollama CLI not found"
- Install Ollama from [ollama.ai](https://ollama.ai)
- Ensure `ollama` is in your PATH
- Start the Ollama server: `ollama serve`

### "Out of memory" errors
- Try smaller models (1b, 2b variants)
- Close other applications
- Reduce `MAX_TOKENS` in configuration
- Use CPU instead of GPU if GPU memory is limited

### "Model not found" or gating errors
- Provide a valid `HF_TOKEN`
- Accept the model license on Hugging Face
- Check model availability (some Gemma 3 models may not be released yet)

### Timeout errors
- Increase timeout values in configuration
- Check network connection
- Verify sufficient compute resources

## Hardware Requirements

### Minimum (for 1b-2b models)
- 8 GB RAM
- Modern CPU
- 10 GB free disk space

### Recommended (for 4b-9b models)
- 16-32 GB RAM
- GPU with 8+ GB VRAM (optional but faster)
- 20 GB free disk space

### High-end (for 12b models)
- 32+ GB RAM
- GPU with 16+ GB VRAM
- 30 GB free disk space

## Notes

- The notebook runs sequentially (one test at a time)
- Memory is aggressively cleared between tests
- All timings include model loading (first run may be slower)
- llamafile tests require downloading entire model files
- Ollama tests reuse cached models across runs
