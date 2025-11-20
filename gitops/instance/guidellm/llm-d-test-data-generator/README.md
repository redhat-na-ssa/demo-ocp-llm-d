# LLM-D Test Data Generator

A tool for generating synthetic test data to benchmark LLM-D (Distributed LLM Serving) systems, specifically designed to test prefix caching behavior and performance under various load conditions.

## Overview

This generator creates paired prompts that demonstrate prefix caching capabilities in distributed LLM systems. It generates:

- **5,000 prompt pairs** with shared prefixes to simulate real-world caching scenarios
- **Long-form content** with 3,000-word prefixes and 3,000-word continuations
- **Strategically spaced prompts** to maximize cache hits and demonstrate routing efficiency

The generated data is ideal for testing:
- Prefix caching effectiveness
- Request routing optimization
- Performance under concurrent load
- Cache reuse patterns in LLM-D deployments

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Generating Test Data

Run the generator:

```bash
python test-data-generator.py
```

This creates two files:

1. **`prefix_caching_5000_pairs_side_by_side.csv`**
   - Side-by-side format of all prompt pairs
   - Useful for manual inspection and analysis
   - Columns: `pair_id`, `prompt_1_prefix`, `prompt_2_prefix_plus_continuation`

2. **`guidellm_formatted_prompts.csv`**
   - Formatted for GuideLLM benchmarking
   - Prompts spaced 200 spots apart to optimize cache hits
   - Columns: `prompt`, `output_tokens_count` (fixed at 250 tokens)

### How It Works

The generator:
1. Creates a base prefix (3,000 words) about prefix caching concepts
2. Creates a continuation (3,000 words) that extends the prefix
3. Generates 5,000 unique pairs with slight variations
4. Interleaves prompts in chunks of 200 to maximize cache effectiveness
5. Formats output for GuideLLM consumption

## Benchmarking with GuideLLM

Use `guidellm_formatted_prompts.csv` as your data source for benchmarking LLM-D deployments.

### Basic Benchmark

```bash
guidellm benchmark \
    --target http://<gateway-hostname>/<namespace>/<llm-d-instance> \
    --model openai/gpt-oss-20b \
    --data guidellm_formatted_prompts.csv \
    --rate-type concurrent \
    --rate 50,25,10,5,1 \
    --max-seconds 120
```

### Disconnected Environment

For disconnected/air-gapped environments, specify a local tokenizer:

```bash
guidellm benchmark \
    --target http://<gateway-hostname>/<namespace>/<llm-d-instance> \
    --model openai/gpt-oss-20b \
    --processor /path/to/local/tokenizer \
    --data guidellm_formatted_prompts.csv \
    --rate-type concurrent \
    --rate 500,250,100,50,25,10,5,1 \
    --max-seconds 120
```
