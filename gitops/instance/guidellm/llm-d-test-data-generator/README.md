# LLM-D Synthetic Test Data Generators

A collection of tools for generating synthetic test data to demonstrate `llm-d` well-lit paths.


## Overview

### Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

There are three synthetic data generators.

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

### 3. KV Cache Prompt Generator ([prefix/kv-cache-prompt-generator.py](prefix/kv-cache-prompt-generator.py))

Generates prompts sized to **fill a target KV-cache occupancy** across replicas.

**Key Features:**
- Calculates the number of unique prompts needed to fill each replica's KV cache to 80%
- Each prompt is repeated a configurable number of times to test cache hit rates
- Configurable gap between repetitions of the same prompt

**Use this generator when you want to:**
- Test KV-cache utilization at a target fill level
- Measure cache hit rates with controlled prompt repetition
- Benchmark prefix-aware routing across multiple replicas

**Quick Start:**
```bash
python prefix/kv-cache-prompt-generator.py \
  --kv-cache-size 100000 \
  --num-replicas 2 \
  --prompt-size 5000 \
  --num-pairs 3
```

**Parameters:**

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--kv-cache-size` | Yes | - | KV-cache capacity per replica, in tokens |
| `--num-replicas` | Yes | - | Number of serving replicas |
| `--prompt-size` | Yes | - | Target size of each prompt, in tokens |
| `--num-pairs` | Yes | - | Number of times each unique prompt is repeated |
| `--repeat-gap` | No | 10 | Number of other prompts between consecutive repetitions |
| `--output-tokens` | No | 250 | Synthetic output-token-count annotation per row |
| `--output` | No | prompts.csv | Output CSV path |

**How it works:**

1. Computes unique prompts per replica: `floor(kv_cache_size * 0.8 / prompt_size)`
2. Multiplies by `num_replicas` to get total unique prompts
3. Generates each prompt at approximately `prompt_size` tokens (~1.3 tokens/word)
4. Repeats each prompt `num_pairs` times with `repeat_gap` other prompts between repetitions

**Output:**
- `prompts.csv` (or path given by `--output`) - guidellm-compatible CSV with `prompt` and `output_tokens_count` columns
