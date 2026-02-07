# testing-small-models-locally

Testing infrastructure for running small language models locally across different runtimes.

## Gemma Runtime Smoke-Test Harness

A comprehensive Jupyter notebook for testing Google Gemma models across three runtimes:
- **Transformers** (Hugging Face, in-notebook Python)
- **Ollama** (external CLI/API)
- **llamafile** (single-file distribution)

### Features

- ✅ Tests Gemma 3 models (1b, 4b, 12b) with Gemma 2 fallbacks
- ✅ Configurable timeouts and parameters
- ✅ Persistent results (JSONL + CSV)
- ✅ OpenAI-generated analysis report
- ✅ Memory clearing between tests
- ✅ Detailed logging and error handling
- ✅ Cross-platform support (CPU, CUDA, MPS)

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the notebook:**
   ```bash
   jupyter notebook notebooks/gemma_runtime_smoketest.ipynb
   ```

3. **Follow the prompts** to provide tokens (HF_TOKEN, OPENAI_API_KEY)

4. **Review results** in the `artifacts/` directory

### Documentation

See [notebooks/README.md](notebooks/README.md) for detailed usage instructions, configuration options, and troubleshooting.

### Output

The notebook generates:
- `artifacts/results.jsonl` - Raw test results
- `artifacts/results.csv` - Flattened summary
- `artifacts/report.md` - AI-generated analysis
- `artifacts/report.json` - Machine-readable report

## Requirements

- Python 3.8+
- 8-32 GB RAM (depending on model size)
- Optional: NVIDIA GPU with CUDA support
- Optional: Ollama installed for Ollama runtime tests

## License

See [LICENSE](LICENSE) for details.