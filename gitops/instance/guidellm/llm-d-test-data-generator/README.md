# LLM-D Synthetic Test Data Generators

A collection of tools for generating synthetic test data to demonstrate `llm-d` well-lit paths.


## Overview

### Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

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


