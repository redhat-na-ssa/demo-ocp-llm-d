# LLM-D Test Data Generator

A tool for generating synthetic test data to benchmark LLM-D (Distributed LLM Serving) systems, specifically designed to test prefix caching behavior and performance under various load conditions.

## Overview

This generator creates paired prompts that demonstrate prefix caching capabilities in distributed LLM systems. It generates:

- **Prompt pairs** with shared prefixes to simulate real-world caching scenarios
- **Long-form content** with word prefixes and word continuations
- **Spaced prompts** to simulate multi-turn request patters

The generated data is ideal for demonstrating benefits of prefix cache aware routing for multi-turn request patterns.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Generating Test Data

Run the generator:

```bash
python test-data-generator.py \
   --target-prefix-words 5000 \
   --target-continuation-words 1000 \
   --num-pairs 300 \
   --chunk-size 50 \
   --output-tokens 250
```

This creates two files:

1. **`pairs.csv`**
   - Side-by-side format of all prompt pairs
   - Useful for manual inspection and analysis
   - Columns: `pair_id`, `prompt_1_prefix`, `prompt_2_prefix_plus_continuation`

2. **`prompts.csv`**
   - Formatted for GuideLLM benchmarking
   - Prompts spaced `chunk-size` spots apart to demonstrate mulit-turn pattern
   - Columns: `prompt`, `output_tokens_count` (fixed at `output-tokens` tokens)

We can generate a separate test dataset for each concurrency range with:

```bash
./generate-all.sh
```

### How It Works

The generator:
1. Creates a base prompt of `--target-prefix-words` with a unique first word per prompt
2. Creates a second prompt with the base prompt + `--target-continuation-words` 
3. Interleaves prompts in `--chunk-size` to simulate multi-turn request pattern
4. Outputs in format compatible with `guidellm`

## Benchmarking with GuideLLM

Use `prompts.csv` as your data source for benchmarking LLM-D deployments.

### Basic Benchmark

```bash
guidellm benchmark \
    --target http://<gateway-hostname>/<namespace>/<llm-d-instance> \
    --model openai/gpt-oss-20b \
    --data prompts.csv \
    --rate-type concurrent \
    --rate 25
```
