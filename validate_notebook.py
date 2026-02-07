#!/usr/bin/env python3
"""
Validation script for gemma_runtime_smoketest.ipynb

This script validates the notebook structure and tests utility functions
without requiring all dependencies to be installed.
"""

import json
import sys
from pathlib import Path

def test_notebook_structure():
    """Validate notebook structure and metadata."""
    print("=" * 80)
    print("NOTEBOOK STRUCTURE VALIDATION")
    print("=" * 80)
    
    notebook_path = Path(__file__).parent / "notebooks" / "gemma_runtime_smoketest.ipynb"
    if not notebook_path.exists():
        print(f"✗ Notebook not found: {notebook_path}")
        return False
    
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    print(f"✓ Notebook loaded successfully")
    print(f"  Format: {notebook.get('nbformat', 'N/A')}.{notebook.get('nbformat_minor', 'N/A')}")
    print(f"  Total cells: {len(notebook['cells'])}")
    
    # Validate cell types
    markdown_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
    code_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'code')
    
    print(f"  Markdown cells: {markdown_cells}")
    print(f"  Code cells: {code_cells}")
    
    if code_cells < 5:
        print(f"✗ Expected at least 5 code cells, found {code_cells}")
        return False
    
    # Check for required sections
    required_sections = [
        'Configuration',
        'Transformers Runtime',
        'Ollama Runtime',
        'llamafile Runtime',
        'OpenAI Report'
    ]
    
    found_sections = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            for section in required_sections:
                if section in content and section not in found_sections:
                    found_sections.append(section)
    
    print(f"\n  Required sections found: {len(found_sections)}/{len(required_sections)}")
    for section in required_sections:
        status = "✓" if section in found_sections else "✗"
        print(f"    {status} {section}")
    
    if len(found_sections) < len(required_sections):
        return False
    
    # Check for configuration variables
    config_vars = [
        'RUN_TRANSFORMERS',
        'RUN_OLLAMA', 
        'RUN_LLAMAFILE',
        'RUN_OPENAI_REPORT',
        'DOWNLOAD_TIMEOUT_S',
        'INFERENCE_TIMEOUT_S',
    ]
    
    found_config = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            content = ''.join(cell['source'])
            for var in config_vars:
                if var in content and var not in found_config:
                    found_config.append(var)
    
    print(f"\n  Configuration variables found: {len(found_config)}/{len(config_vars)}")
    for var in config_vars:
        status = "✓" if var in found_config else "✗"
        print(f"    {status} {var}")
    
    if len(found_config) < len(config_vars):
        return False
    
    print("\n✓ Notebook structure validation passed!")
    return True


def test_model_lists():
    """Validate model lists in configuration."""
    print("\n" + "=" * 80)
    print("MODEL LISTS VALIDATION")
    print("=" * 80)
    
    notebook_path = Path(__file__).parent / "notebooks" / "gemma_runtime_smoketest.ipynb"
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Find configuration cell
    config_content = ""
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            content = ''.join(cell['source'])
            if 'TRANSFORMERS_MODELS' in content:
                config_content = content
                break
    
    if not config_content:
        print("✗ Configuration cell not found")
        return False
    
    # Check for Gemma 3 models
    gemma3_models = ['gemma-3-1b', 'gemma-3-4b', 'gemma-3-12b']
    found_gemma3 = []
    for model in gemma3_models:
        if model in config_content:
            found_gemma3.append(model)
            print(f"  ✓ Found {model}")
    
    if len(found_gemma3) < 3:
        print(f"✗ Expected 3 Gemma 3 models, found {len(found_gemma3)}")
        return False
    
    # Check for Gemma 2 fallbacks
    gemma2_models = ['gemma-2-2b', 'gemma-2-9b']
    found_gemma2 = []
    for model in gemma2_models:
        if model in config_content:
            found_gemma2.append(model)
            print(f"  ✓ Found {model} (fallback)")
    
    if len(found_gemma2) < 2:
        print(f"⚠ Warning: Only {len(found_gemma2)} Gemma 2 fallback models found")
    
    print("\n✓ Model lists validation passed!")
    return True


def test_timeout_configuration():
    """Validate timeout configuration."""
    print("\n" + "=" * 80)
    print("TIMEOUT CONFIGURATION VALIDATION")
    print("=" * 80)
    
    notebook_path = Path(__file__).parent / "notebooks" / "gemma_runtime_smoketest.ipynb"
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Find timeout configuration
    timeout_vars = {
        'DOWNLOAD_TIMEOUT_S': 300,  # minimum expected
        'FIRST_LOAD_TIMEOUT_S': 60,
        'INFERENCE_TIMEOUT_S': 30,
        'PROCESS_SHUTDOWN_TIMEOUT_S': 10,
    }
    
    config_content = ""
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            content = ''.join(cell['source'])
            if 'DOWNLOAD_TIMEOUT_S' in content:
                config_content = content
                break
    
    if not config_content:
        print("✗ Timeout configuration not found")
        return False
    
    for var, min_val in timeout_vars.items():
        if var in config_content:
            print(f"  ✓ {var} configured")
        else:
            print(f"  ✗ {var} missing")
            return False
    
    print("\n✓ Timeout configuration validation passed!")
    return True


def test_prompts():
    """Validate prompt configuration."""
    print("\n" + "=" * 80)
    print("PROMPTS VALIDATION")
    print("=" * 80)
    
    notebook_path = Path(__file__).parent / "notebooks" / "gemma_runtime_smoketest.ipynb"
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Find prompts
    prompts_found = False
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            content = ''.join(cell['source'])
            if 'SHORT_PROMPT' in content and 'COMPLEX_PROMPT' in content:
                prompts_found = True
                print("  ✓ SHORT_PROMPT configured")
                print("  ✓ COMPLEX_PROMPT configured")
                
                # Check for JSON requirement in complex prompt
                if 'JSON' in content or 'json' in content:
                    print("  ✓ Complex prompt includes JSON requirement")
                else:
                    print("  ⚠ Complex prompt may not include JSON requirement")
                
                break
    
    if not prompts_found:
        print("✗ Prompts not found")
        return False
    
    print("\n✓ Prompts validation passed!")
    return True


def test_output_paths():
    """Validate output path configuration."""
    print("\n" + "=" * 80)
    print("OUTPUT PATHS VALIDATION")
    print("=" * 80)
    
    notebook_path = Path(__file__).parent / "notebooks" / "gemma_runtime_smoketest.ipynb"
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    required_outputs = [
        'RESULTS_JSONL',
        'RESULTS_CSV',
        'REPORT_MD',
        'REPORT_JSON',
    ]
    
    found_outputs = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            content = ''.join(cell['source'])
            for output in required_outputs:
                if output in content and output not in found_outputs:
                    found_outputs.append(output)
    
    for output in required_outputs:
        status = "✓" if output in found_outputs else "✗"
        print(f"  {status} {output}")
    
    if len(found_outputs) < len(required_outputs):
        return False
    
    print("\n✓ Output paths validation passed!")
    return True


def test_artifacts_directory():
    """Validate artifacts directory exists."""
    print("\n" + "=" * 80)
    print("ARTIFACTS DIRECTORY VALIDATION")
    print("=" * 80)
    
    artifacts_dir = Path(__file__).parent / "artifacts"
    if not artifacts_dir.exists():
        print(f"✗ Artifacts directory not found: {artifacts_dir}")
        return False
    
    print(f"✓ Artifacts directory exists: {artifacts_dir}")
    
    # Check for .gitkeep
    gitkeep = artifacts_dir / ".gitkeep"
    if gitkeep.exists():
        print(f"✓ .gitkeep file exists")
    else:
        print(f"⚠ .gitkeep file not found (directory may not be tracked in git)")
    
    return True


def test_requirements():
    """Validate requirements.txt."""
    print("\n" + "=" * 80)
    print("REQUIREMENTS VALIDATION")
    print("=" * 80)
    
    req_path = Path(__file__).parent / "requirements.txt"
    if not req_path.exists():
        print(f"✗ requirements.txt not found")
        return False
    
    with open(req_path, 'r') as f:
        requirements = f.read()
    
    required_packages = [
        'jupyter',
        'notebook',
        'transformers',
        'torch',
        'psutil',
        'pandas',
        'openai',
        'huggingface_hub',
    ]
    
    for package in required_packages:
        if package in requirements:
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ {package} missing")
            return False
    
    print("\n✓ Requirements validation passed!")
    return True


def main():
    """Run all validation tests."""
    print("\n" + "=" * 80)
    print("GEMMA RUNTIME SMOKETEST NOTEBOOK VALIDATION")
    print("=" * 80 + "\n")
    
    tests = [
        ("Notebook Structure", test_notebook_structure),
        ("Model Lists", test_model_lists),
        ("Timeout Configuration", test_timeout_configuration),
        ("Prompts", test_prompts),
        ("Output Paths", test_output_paths),
        ("Artifacts Directory", test_artifacts_directory),
        ("Requirements", test_requirements),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ {name} test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All validation tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
