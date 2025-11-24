# LLM-D Synthetic Test Data Generators

A collection of tools for generating synthetic test data to demonstrate `llm-d` well-lit paths.

## Overview

There are two synthetic data generators.

### 1. Prefix Cache Generator ([prefix-cache-generator.py](prefix-cache-generator.py))

Tests **prefix caching effectiveness** by generating prompt pairs with shared prefixes.
- Generates prompt pairs with shared prefixes to simulate multi-turn request patterns
- Useful for benchmarking efficiency of prefix-cache aware routing

**Quick Start:**
```bash
python prefix-cache-generator.py 
```

**Output:**
- `prefix-pairs.csv` - All prompt pairs for inspection
- `prefix-prompts.csv` - Ready for benchmarking with guidellm

[→ See detailed documentation below](#prefix-cache-generator)

---

### 2. Heterogeneous Workload Generator ([heterogeneous-workload-generator.py](heterogeneous-workload-generator.py))

Tests **mixed workload handling** by generating requests of different sizes with configurable ratios.

**Key Features:**
- Generates unique prompts with different workload shapes (size N and size M)
- Useful for benchmarking heterogeneous workloads in `llm-d` (e.g. for P/D disagg)

**Use this generator when you want to:**
- Test performance with mixed request sizes
- Simulate realistic production traffic patterns
- Measure how systems handle workload transitions
- Benchmark resource allocation strategies

**Quick Start:**
```bash
python heterogeneous-workload-generator.py
```

**Output:**
- `heterogeneous-prompts.csv` - Ready for benchmarking with guidellm

[→ See detailed documentation below](#heterogeneous-workload-generator)

---

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Prefix Cache Generator

### How It Works

The prefix cache generator creates prompt pairs to test prefix caching:

1. Creates a base prefix (3,000 words) about prefix caching concepts
2. Creates a continuation (3,000 words) that extends the prefix
3. Generates 5,000 unique pairs with slight variations
4. Interleaves prompts in chunks of 200 to maximize cache effectiveness
5. Formats output for guidellm consumption

### Usage

```bash
python prefix-cache-generator.py
```

### Output Files

**`prefix_caching_5000_pairs_side_by_side.csv`**
- Side-by-side format of all prompt pairs
- Useful for manual inspection and analysis
- Columns: `pair_id`, `prompt_1_prefix`, `prompt_2_prefix_plus_continuation`

**`guidellm_formatted_prompts.csv`**
- Formatted for guidellm benchmarking
- Prompts spaced 200 spots apart to optimize cache hits
- Columns: `prompt`, `output_tokens_count` (fixed at 250 tokens)

### Benchmarking with guidellm

```bash
guidellm benchmark \
    --target http://<gateway-hostname>/<namespace>/<llm-d-instance> \
    --model openai/gpt-oss-20b \
    --data guidellm_formatted_prompts.csv \
    --rate-type concurrent \
    --rate 50,25,10,5,1 \
    --max-seconds 120
```

---

## Heterogeneous Workload Generator

### How It Works

The heterogeneous generator creates mixed workloads to test handling of different request sizes:

1. Generates prompts of size N (e.g., 1,000 words)
2. Generates prompts of size M (e.g., 20,000 words)
3. Each prompt has a unique index in the first words to prevent prefix caching
4. Interleaves prompts according to specified ratio (e.g., 4:1)
5. Outputs in guidellm-compatible format

### Usage

#### Basic Usage

Generate with default settings (4:1 ratio of 1000-word to 20,000-word prompts):

```bash
python heterogeneous-workload-generator.py
```

#### Custom Workload Sizes

```bash
python heterogeneous-workload-generator.py \
  --workload-n-words 500 \
  --workload-m-words 5000
```

#### Custom Ratio and Total Prompts

```bash
# Generate 10,000 prompts with a 3:1 ratio (75% small, 25% large)
python heterogeneous-workload-generator.py \
  --total-prompts 10000 \
  --ratio-n-to-m 3
```

#### Full Example

```bash
python heterogeneous-workload-generator.py \
  --workload-n-words 800 \
  --workload-m-words 8000 \
  --total-prompts 5000 \
  --ratio-n-to-m 4 \
  --output-tokens 400 \
  --output-file my_workload.csv \
  --seed 12345
```

### Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--workload-n-words` | int | 1000 | Number of input words for workload type N |
| `--workload-m-words` | int | 20000 | Number of input words for workload type M |
| `--total-prompts` | int | 10000 | Total number of prompts to generate |
| `--ratio-n-to-m` | int | 4 | Ratio of N to M prompts (e.g., 4 means 4 N for every 1 M) |
| `--output-tokens` | int | 500 | Number of output tokens to generate |
| `--output-file` | str | heterogeneous_workload.csv | Output CSV file path |
| `--seed` | int | 42 | Random seed for reproducibility |

### Output Format

The script generates a CSV file with the following columns:

- `prompt`: The generated prompt text
- `output_tokens_count`: Number of tokens to generate (for benchmarking)

### Example Use Cases

#### Test Different Request Size Distributions

```bash
# Very small and very large requests
python heterogeneous-workload-generator.py \
  --workload-n-words 100 \
  --workload-m-words 10000 \
  --ratio-n-to-m 9
```

#### Simulate Realistic Production Traffic

```bash
# 80% medium requests, 20% large requests
python heterogeneous-workload-generator.py \
  --workload-n-words 500 \
  --workload-m-words 3000 \
  --ratio-n-to-m 4 \
  --total-prompts 20000
```

#### Test Resource Allocation

```bash
# Equal mix of small and large
python heterogeneous-workload-generator.py \
  --workload-n-words 200 \
  --workload-m-words 5000 \
  --ratio-n-to-m 1 \
  --total-prompts 1000
```

### Benchmarking with guidellm

```bash
guidellm benchmark \
  --target http://your-model-endpoint \
  --data heterogeneous_workload.csv \
  --rate-type concurrent \
  --rate 50,25,10
```

---

## Prevention of Prefix Caching in Heterogeneous Generator

Each prompt in the heterogeneous generator begins with a unique index:

```
Request number {index}: [rest of prompt content...]
```

This ensures that:
- No two prompts share a common prefix
- Prefix caching mechanisms won't artificially improve benchmark results
- Each request is processed independently

---

## Choosing the Right Generator

| Scenario | Generator to Use |
|----------|-----------------|
| Testing cache effectiveness | Prefix Cache Generator |
| Testing routing intelligence | Prefix Cache Generator |
| Testing mixed workload performance | Heterogeneous Workload Generator |
| Simulating production traffic patterns | Heterogeneous Workload Generator |
| Measuring cache hit rates | Prefix Cache Generator |
| Testing resource allocation | Heterogeneous Workload Generator |
| Benchmarking with variable request sizes | Heterogeneous Workload Generator |

---

## Integration with guidellm

Both generators output CSV files formatted for direct use with the guidellm benchmarking tool. The `output_tokens_count` column specifies how many tokens should be generated for each prompt during benchmarking.

### Basic guidellm Usage

```bash
guidellm benchmark \
    --target http://<endpoint> \
    --model <model-name> \
    --data <output-csv-file> \
    --rate-type concurrent \
    --rate 50,25,10,5,1 \
    --max-seconds 120
```
