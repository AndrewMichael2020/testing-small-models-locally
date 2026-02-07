[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-F37626.svg?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.50%2B-yellow.svg)](https://huggingface.co/docs/transformers)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)

# testing-small-models-locally

**Can I actually run this model on this machine?**

A structured, repeatable Jupyter notebook for smoke-testing Google Gemma models across three local runtimes — **Transformers**, **Ollama**, and **llamafile** — to determine what's runnable on a given machine before committing to a deployment strategy for local, sovereign agentic applications.

It loads each model, runs two inference prompts, records wall-clock timings, and captures every success, failure, and skip with enough metadata to diagnose _why_ something didn't work. An optional final step sends the raw results to OpenAI for an analyst-readable report.

All output is deterministic given the same seed (`SEED = 42`), model weights, and hardware.

---

## What This Notebook Does

For every (model, runtime) combination in the configured matrix:

1. **Download / pull** the model (with a configurable hard timeout).
2. **Load** it into memory, detect the device (CPU / CUDA / MPS), and log a memory snapshot.
3. **Run inference** on two prompts:
   - **Short** — `"What is the capital of France?"` (sanity check, tests basic generation)
   - **Complex** — Structured JSON extraction from natural-language text (tests instruction-following and output format adherence)
4. **Record a result** with status (`SUCCESS` / `FAILED` / `SKIPPED`), wall-clock duration, device, model ID, prompt text, generated output, and any error message.
5. **Clear memory** aggressively (`gc.collect()`, `torch.cuda.empty_cache()`) and log the memory delta.
6. **Persist results** incrementally to `artifacts/results.jsonl` — one JSON object per line, append-only, so partial runs are never lost.
7. Optionally, **generate an analysis report** via the OpenAI API, saved as `artifacts/report.md` and `artifacts/report.json`.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve   # in another terminal

# 3. Run the notebook
jupyter notebook notebooks/gemma_runtime_smoketest.ipynb
# or open in VS Code and run cells sequentially
```

When prompted, provide:

| Token | Source | Without It |
|---|---|---|
| `HF_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | Gated models fail to download; Transformers tests may be skipped |
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | Report generation is skipped; all raw results are still saved |

---

## Runtimes

| Runtime | How It Runs | Install Requirement |
|---|---|---|
| **Transformers** | In-process Python via Hugging Face `transformers` + `torch` | `pip install -r requirements.txt` |
| **Ollama** | External daemon; notebook shells out via `ollama pull` / `ollama run` | [ollama.ai](https://ollama.ai) installed + `ollama serve` running |
| **llamafile** | Single-binary executable downloaded from Hugging Face, run as a subprocess | None beyond `huggingface_hub` (included in requirements) |

Each runtime is independently toggled via `RUN_TRANSFORMERS`, `RUN_OLLAMA`, `RUN_LLAMAFILE` in the Configuration cell.

---

## Models Tested

### Gemma 3 (Primary)

| Size | Transformers ID | Ollama Tag | llamafile Repo |
|---|---|---|---|
| 1B | `google/gemma-3-1b-it` | `gemma3:1b` | `mozilla-ai/gemma-3-1b-it-llamafile` |
| 4B | `google/gemma-3-4b-it` | `gemma3:4b` | `mozilla-ai/gemma-3-4b-it-llamafile` |
| 12B | `google/gemma-3-12b-it` | `gemma3:12b` | `mozilla-ai/gemma-3-12b-it-llamafile` |

### Gemma 2 (Fallback)

| Size | Transformers ID | Ollama Tag | llamafile Repo |
|---|---|---|---|
| 2B | `google/gemma-2-2b-it` | `gemma2:2b` | `mozilla-ai/gemma-2-2b-it-llamafile` |
| 9B | `google/gemma-2-9b-it` | `gemma2:9b` | — |

12B and larger models are commented out by default; uncomment them if your hardware can support them.

---

## Configuration Reference

All tunable parameters live in **one cell** (Configuration Section, cell 5). Nothing else needs editing.

### Runtime Flags

| Variable | Default | Effect |
|---|---|---|
| `RUN_TRANSFORMERS` | `True` | Enable Hugging Face Transformers tests |
| `RUN_OLLAMA` | `True` | Enable Ollama CLI tests |
| `RUN_LLAMAFILE` | `True` | Enable llamafile tests |
| `RUN_OPENAI_REPORT` | `True` | Enable OpenAI report generation |

### Timeouts

| Variable | Default | Scope |
|---|---|---|
| `DOWNLOAD_TIMEOUT_S` | `1800` (30 min) | Model download / `ollama pull` / llamafile download |
| `FIRST_LOAD_TIMEOUT_S` | `600` (10 min) | First model load into memory |
| `INFERENCE_TIMEOUT_S` | `120` (2 min) | Each individual inference call |
| `PROCESS_SHUTDOWN_TIMEOUT_S` | `30` | Cleanup of subprocess after timeout |

### Generation Parameters

| Variable | Default | Notes |
|---|---|---|
| `MAX_TOKENS` | `512` | Max new tokens per generation |
| `TEMPERATURE` | `0.7` | Sampling temperature |
| `SEED` | `42` | For reproducibility |

### Output Paths

| Variable | Path |
|---|---|
| `RESULTS_JSONL` | `artifacts/results.jsonl` |
| `RESULTS_CSV` | `artifacts/results.csv` |
| `REPORT_MD` | `artifacts/report.md` |
| `REPORT_JSON` | `artifacts/report.json` |

---

## Output Format

### `results.jsonl` — One JSON object per line

```json
{
  "timestamp": "2026-02-07T17:15:39.664574",
  "runtime": "transformers",
  "model": "google/gemma-3-1b-it",
  "status": "SUCCESS",
  "prompt_name": "short",
  "prompt_text": "What is the capital of France?",
  "output": "Paris",
  "duration_s": 0.972,
  "device": "cpu",
  "error": ""
}
```

**Status values:**
- `SUCCESS` — Model loaded and generated output.
- `FAILED` — Something went wrong (download, OOM, timeout, runtime error). The `error` field says what.
- `SKIPPED` — Intentionally not run (runtime missing, token not provided, etc.).

### `results.csv` — Same data flattened for quick inspection in Excel / pandas.

### `report.md` — Analyst-readable report generated by OpenAI covering:
- Which models ran successfully.
- Failures clustered by root cause.
- Latency table with estimated tokens/sec.
- Practical recommendations for local deployment.

### `report.json` — Machine-readable report metadata (timestamps, token counts, summary stats).

---

## First Run Results (Feb 7, 2026 — CPU-only devcontainer)

These results are from the actual `artifacts/results.jsonl` produced by running this notebook:

| Runtime | Model | Prompt | Duration | Notes |
|---|---|---|---|---|
| Transformers | gemma-3-1b-it | short | **0.97s** | Correct ("Paris") |
| Transformers | gemma-3-1b-it | complex | **110.4s** | Correct JSON, repeated 11× — `MAX_TOKENS=512` too generous on CPU |
| Transformers | gemma-3-4b-it | short | **313.6s** | 5+ min on CPU; output degenerated into trivia questions + blank lines |
| Transformers | gemma-3-4b-it | complex | **29.8s** | Correct JSON, clean output |
| Ollama | — | — | — | Not installed in devcontainer |
| llamafile | — | — | — | Repos not found |

**Key takeaways:**
- 1B on CPU is usable for short prompts (<1s). Structured output works but is slow (~110s) because `max_new_tokens` allows the model to keep generating.
- 4B on CPU is impractical (5 min for one prompt). Memory bandwidth — not compute — is the bottleneck.
- The notebook currently lacks resource guardrails, streaming subprocess output, and system diagnostics that would explain _why_ performance degrades and _when_ to skip a model.

---

## Hardware Requirements

| Tier | RAM | GPU | Realistic Models | Short Prompt Speed |
|---|---|---|---|---|
| **Minimum** | 8 GB | None | 1B only | 1–5s (CPU) |
| **Recommended** | 16–32 GB | 8+ GB VRAM | 1B, 4B | <1s (GPU) / 30–300s (CPU for 4B) |
| **High-end** | 32+ GB | 16+ GB VRAM | 1B, 4B, 12B | <1s (GPU) |

**Disk:** 5–30 GB depending on how many models are cached (Transformers downloads to `~/.cache/huggingface`, Ollama to `~/.ollama`, llamafile to `artifacts/llamafile_cache`).

---

## Project Structure

```
testing-small-models-locally/
├── README.md                           # ← You are here
├── requirements.txt                    # Python dependencies
├── LICENSE                             # MIT
├── validate_notebook.py                # Notebook structure validator (7 tests)
├── generate_examples.py                # Generates sample output files
├── IMPLEMENTATION.md                   # Implementation notes
├── FINAL_SUMMARY.md                    # Delivery summary
├── notebooks/
│   ├── gemma_runtime_smoketest.ipynb    # The notebook (22 cells)
│   └── artifacts/
│       └── results.jsonl                # Actual run results
└── artifacts/
    ├── example_results.jsonl             # Example output (committed)
    ├── example_results.csv
    ├── example_report.md
    └── example_report.json
```

---

## Notebook Cell Map

| # | Type | Purpose |
|---|---|---|
| 1 | Markdown | Title, goals, model scope, output description |
| 2–3 | Setup | Imports, environment check, artifacts directory |
| 4–5 | Config | All tunable parameters (flags, models, timeouts, prompts, paths) |
| 6–7 | Tokens | `HF_TOKEN` and `OPENAI_API_KEY` prompts |
| 8–9 | Utils | `get_environment_fingerprint()`, `log_phase()`, `get_memory_info()`, `clear_memory()`, `save_result()`, `create_result_record()` |
| 10–11 | Env | Print environment metadata as JSON |
| 12–13 | **Transformers** | `test_transformers_model()` — load, infer, record, cleanup |
| 14–15 | **Ollama** | `check_ollama_available()`, `test_ollama_model()` — pull, infer, record |
| 16–17 | **llamafile** | `download_llamafile()`, `test_llamafile_model()` — download, chmod, run, record |
| 18–19 | Summary | Load `results.jsonl`, create DataFrame, save CSV, print summary |
| 20–21 | Report | Build prompt from results, call OpenAI API, save report |
| 22 | Markdown | Closing summary |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Ollama CLI not found` | Ollama not installed | Install from [ollama.ai](https://ollama.ai), run `ollama serve` |
| System becomes unresponsive | Model exceeds available RAM → OS swaps | Use 1B only, reduce `MAX_TOKENS` |
| `401 Client Error` / gating | HF token missing or license not accepted | Set `HF_TOKEN`, accept license on the [model page](https://huggingface.co/google/gemma-3-1b-it) |
| Repeated / garbage output | `MAX_TOKENS` too high for prompt complexity | Reduce `MAX_TOKENS` or add stop sequences |
| Cell hangs with no output | `subprocess.run(capture_output=True)` buffers everything | Known limitation — see below |

---

## Known Limitations

1. **No streaming subprocess output** — Ollama and llamafile cells show nothing until the process completes or times out.
2. **No resource guardrails** — The notebook will attempt to load any configured model regardless of available RAM; no pre-check to prevent swapping.
3. **No system diagnostics** — Memory bandwidth, disk I/O, cgroup limits, and CPU throttling are not measured, even though they are the primary bottlenecks for CPU inference.
4. **No per-inference memory tracking** — Memory snapshots exist at phase boundaries but not around individual inference calls.
5. **OpenAI call has no timeout** — If the API is slow or unreachable, the cell hangs indefinitely.
6. **Sequential execution only** — By design, to avoid resource contention.
7. **Gemma 3 availability** — Some models may be gated or not yet released on certain runtimes.

---

## License

[MIT](LICENSE) © 2026 Andrew Michael