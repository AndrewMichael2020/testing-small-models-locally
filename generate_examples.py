#!/usr/bin/env python3
"""
Generate example output files to demonstrate expected format.

This script creates sample output files that show what a successful
notebook run would produce.
"""

import json
from datetime import datetime
from pathlib import Path

def generate_example_results():
    """Generate example results.jsonl file."""
    
    artifacts_dir = Path(__file__).parent / "artifacts"
    
    example_results = [
        # Transformers - successful runs
        {
            "timestamp": "2024-02-07T10:00:00.000Z",
            "runtime": "transformers",
            "model": "google/gemma-3-1b-it",
            "status": "SUCCESS",
            "prompt_name": "short",
            "prompt_text": "What is the capital of France?",
            "output": "The capital of France is Paris.",
            "duration_s": 2.5,
            "device": "cuda",
            "error": ""
        },
        {
            "timestamp": "2024-02-07T10:01:00.000Z",
            "runtime": "transformers",
            "model": "google/gemma-3-1b-it",
            "status": "SUCCESS",
            "prompt_name": "complex",
            "prompt_text": "Extract information from the following text...",
            "output": '{"name": "John Smith", "age": 35, "city": "San Francisco", "occupation": "software engineer"}',
            "duration_s": 3.2,
            "device": "cuda",
            "error": ""
        },
        # Transformers - failed model (gating)
        {
            "timestamp": "2024-02-07T10:05:00.000Z",
            "runtime": "transformers",
            "model": "google/gemma-3-12b-it",
            "status": "FAILED",
            "prompt_name": "",
            "prompt_text": "",
            "output": "",
            "duration_s": 0.0,
            "device": "cuda",
            "error": "HfHubHTTPError: 401 Client Error: Repository Not Found"
        },
        # Ollama - successful runs
        {
            "timestamp": "2024-02-07T10:10:00.000Z",
            "runtime": "ollama",
            "model": "gemma3:1b",
            "status": "SUCCESS",
            "prompt_name": "short",
            "prompt_text": "What is the capital of France?",
            "output": "The capital of France is Paris.",
            "duration_s": 1.8,
            "device": "",
            "error": ""
        },
        {
            "timestamp": "2024-02-07T10:11:00.000Z",
            "runtime": "ollama",
            "model": "gemma3:1b",
            "status": "SUCCESS",
            "prompt_name": "complex",
            "prompt_text": "Extract information from the following text...",
            "output": '{"name": "John Smith", "age": 35, "city": "San Francisco", "occupation": "software engineer"}',
            "duration_s": 2.5,
            "device": "",
            "error": ""
        },
        # Ollama - model not available
        {
            "timestamp": "2024-02-07T10:15:00.000Z",
            "runtime": "ollama",
            "model": "gemma3:12b",
            "status": "FAILED",
            "prompt_name": "",
            "prompt_text": "",
            "output": "",
            "duration_s": 0.0,
            "device": "",
            "error": "Pull failed: model 'gemma3:12b' not found"
        },
        # llamafile - skipped (not installed)
        {
            "timestamp": "2024-02-07T10:20:00.000Z",
            "runtime": "llamafile",
            "model": "mozilla-ai/gemma-3-1b-it-llamafile",
            "status": "SKIPPED",
            "prompt_name": "",
            "prompt_text": "",
            "output": "",
            "duration_s": 0.0,
            "device": "",
            "error": "Download failed: Repository not found"
        },
    ]
    
    # Write JSONL
    example_jsonl = artifacts_dir / "example_results.jsonl"
    with open(example_jsonl, 'w') as f:
        for result in example_results:
            f.write(json.dumps(result) + '\n')
    
    print(f"✓ Created {example_jsonl}")
    
    # Write CSV header and rows
    example_csv = artifacts_dir / "example_results.csv"
    import csv
    
    with open(example_csv, 'w', newline='') as f:
        if example_results:
            writer = csv.DictWriter(f, fieldnames=example_results[0].keys())
            writer.writeheader()
            writer.writerows(example_results)
    
    print(f"✓ Created {example_csv}")
    
    # Create example report
    example_report = artifacts_dir / "example_report.md"
    report_text = """# Gemma Runtime Smoke-Test Report

## Executive Summary

Successfully tested Google Gemma models across Transformers and Ollama runtimes on a machine with NVIDIA GPU (CUDA enabled).

**Key Findings:**
- ✓ Gemma 3 1b models work well across both Transformers and Ollama
- ✗ Gemma 3 12b model failed due to repository gating
- ✗ llamafile runtime unavailable (models not found in repositories)

**Best Runtime:** Ollama (fastest inference, 1.8s for short prompt)

## Failure Analysis

### Failure Categories

1. **Repository Gating (1 failure)**
   - Model: google/gemma-3-12b-it
   - Cause: 401 Client Error, likely requires model access approval
   - Solution: Request access on Hugging Face model page

2. **Model Not Available (1 failure)**
   - Model: gemma3:12b
   - Cause: Tag not found in Ollama registry
   - Solution: Use smaller model or wait for release

3. **Runtime Unavailable (1 skipped)**
   - Runtime: llamafile
   - Cause: Repository not found for llamafile artifacts
   - Solution: Check mozilla-ai repositories for availability

## Performance Metrics

| Runtime      | Model                | Prompt  | Duration (s) | Est. Tokens/sec |
|--------------|----------------------|---------|--------------|-----------------|
| transformers | gemma-3-1b-it        | short   | 2.5          | ~20             |
| transformers | gemma-3-1b-it        | complex | 3.2          | ~25             |
| ollama       | gemma3:1b            | short   | 1.8          | ~28             |
| ollama       | gemma3:1b            | complex | 2.5          | ~32             |

**Best Performance:** Ollama gemma3:1b (fastest, most efficient)

## Recommendations for Local/Sovereign Agentic Apps

### Runtime Choice: **Ollama**
- **Pros:** Fastest inference, easy installation, good model management
- **Cons:** Requires separate daemon, limited model availability for newest releases

**Alternative:** Transformers (better for latest models, more control)

### Model Size: **1b-4b models are realistic for this machine**
- 1b models: Fast, suitable for real-time applications
- 4b models: Good balance of speed and capability
- 12b models: May require access approval and significant resources

### Practical Tradeoffs

1. **Latency vs Capability**
   - 1b models: <3s inference, good for simple tasks
   - 4b models: 3-6s inference, better reasoning
   - 12b models: >10s inference, best capability

2. **Memory Requirements**
   - 1b: ~2-4 GB VRAM
   - 4b: ~8-12 GB VRAM
   - 12b: ~24+ GB VRAM

3. **Development Workflow**
   - Use Ollama for fast iteration
   - Switch to Transformers for production/latest models
   - Consider llamafile for distribution (when available)

### Recommended Setup for Agentic Apps

```python
# Primary runtime for development
runtime = "ollama"
model = "gemma3:1b"  # Fast, capable

# Fallback for latest models
runtime_fallback = "transformers"
model_fallback = "google/gemma-3-1b-it"
```

## Conclusion

This hardware configuration (CUDA GPU, 32GB RAM) is well-suited for running Gemma 1b-4b models locally. Ollama provides the best performance for rapid development, while Transformers offers access to the latest models. For production agentic applications, consider:

1. Start with 1b models for prototyping
2. Scale to 4b when more reasoning is needed
3. Use Ollama for speed, Transformers for flexibility
4. Monitor memory usage and implement graceful degradation
"""
    
    with open(example_report, 'w') as f:
        f.write(report_text)
    
    print(f"✓ Created {example_report}")
    
    # Create example report JSON
    example_report_json = artifacts_dir / "example_report.json"
    report_data = {
        "generated_at": "2024-02-07T10:30:00.000Z",
        "model_used": "gpt-4o",
        "environment": {
            "os": "Linux-5.15.0-generic",
            "python_version": "3.10.0",
            "cuda_available": True,
            "gpu_name": "NVIDIA GeForce RTX 3090",
            "ram_gb": 32.0
        },
        "report_text": report_text,
        "results_summary": {
            "total_tests": 7,
            "successful": 4,
            "failed": 2,
            "skipped": 1
        }
    }
    
    with open(example_report_json, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"✓ Created {example_report_json}")
    print(f"\n✓ Example output files generated successfully!")


if __name__ == "__main__":
    generate_example_results()
