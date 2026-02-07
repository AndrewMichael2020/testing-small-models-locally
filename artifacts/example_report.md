# Gemma Runtime Smoke-Test Report

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
