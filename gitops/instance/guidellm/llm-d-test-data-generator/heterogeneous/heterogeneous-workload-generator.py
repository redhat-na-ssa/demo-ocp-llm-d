import csv
import random
import argparse
import pandas as pd


# -------------------------------
# Helpers
# -------------------------------


def word_count(s: str) -> int:
    return len(s.split())


# Base sentences that can be used to construct prompts of varying lengths
BASE_SENTENCES = [
    "The application processes data from multiple sources and transforms it according to predefined rules and business logic.",
    "A distributed system coordinates tasks across several nodes to ensure consistent and reliable operation.",
    "The algorithm analyzes patterns in historical data to predict future trends and optimize resource allocation.",
    "Modern architectures balance scalability requirements with maintainability concerns and operational complexity.",
    "The framework provides abstractions that simplify common tasks while maintaining flexibility for custom implementations.",
    "Performance monitoring tools track metrics across the system and alert operators when thresholds are exceeded.",
    "The service layer mediates between presentation and data access to enforce business rules and validation logic.",
    "Caching strategies improve response times by storing frequently accessed data in memory rather than fetching it repeatedly.",
    "The configuration system allows administrators to adjust behavior without modifying code or redeploying services.",
    "Authentication mechanisms verify user identity through various methods including passwords, tokens, and biometric data.",
    "Load balancers distribute incoming requests across multiple servers to prevent any single instance from being overwhelmed.",
    "The database schema organizes information into tables with relationships that reflect the domain model and access patterns.",
    "Error handling routines catch exceptions, log diagnostic information, and return meaningful messages to the caller.",
    "The API gateway routes requests to appropriate backend services and aggregates responses before returning to clients.",
    "Deployment pipelines automate testing, building, and releasing software to reduce manual effort and human error.",
    "The message queue decouples producers from consumers and provides buffering when processing rates differ significantly.",
    "Security policies restrict access to sensitive resources based on roles, permissions, and contextual factors.",
    "The logging infrastructure captures events at different levels and stores them for analysis and troubleshooting.",
    "Data validation ensures that inputs conform to expected formats and constraints before being processed or persisted.",
    "The scheduler manages background jobs and ensures they execute at appropriate times without interfering with interactive workloads.",
    "Backup procedures create copies of critical data and test restoration processes to minimize downtime during failures.",
    "The network layer handles communication between components using protocols that ensure reliable and ordered delivery.",
    "Testing frameworks enable developers to write automated checks that verify functionality and catch regressions early.",
    "The orchestration system coordinates complex workflows involving multiple services and manages state across steps.",
    "Documentation provides guidance for developers, operators, and end users about features, configuration, and troubleshooting.",
    "The middleware pipeline processes requests through a series of steps that perform authentication, logging, and transformation.",
    "Resource management utilities monitor consumption of CPU, memory, and storage to prevent exhaustion and degradation.",
    "The notification system delivers alerts through various channels including email, SMS, and push messages.",
    "Version control tracks changes to source code and enables collaboration among team members working on shared files.",
    "The analytics platform aggregates metrics from disparate sources and presents them in dashboards for decision making.",
]


def make_prompt_with_index(index: int, target_words: int, rng: random.Random) -> str:
    """
    Create a prompt with exactly target_words words.
    The index appears in the first 10 words to prevent prefix caching.
    """
    # Start with a unique prefix containing the index
    prefix = f"Request number {index}:"

    words = prefix.split()

    # Add sentences until we reach the target
    while len(words) < target_words:
        sentence = rng.choice(BASE_SENTENCES)
        words.extend(sentence.split())

    # Trim to exact word count
    trimmed = " ".join(words[:target_words])
    return trimmed


# -------------------------------
# Main generation
# -------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate heterogeneous workload with two interleaved prompt types"
    )
    parser.add_argument(
        "--workload-n-words",
        type=int,
        default=500,
        help="Number of input words for workload type N (default: 500)"
    )
    parser.add_argument(
        "--workload-m-words",
        type=int,
        default=10000,
        help="Number of input words for workload type M (default: 10000)"
    )
    parser.add_argument(
        "--total-prompts",
        type=int,
        default=10000,
        help="Total number of prompts to generate (default: 10000)"
    )
    parser.add_argument(
        "--ratio-n-to-m",
        type=int,
        default="9",
        help="Ratio of N to M prompts (e.g., '9' means 9 N prompts for every 1 M prompt"
    )
    parser.add_argument(
        "--output-tokens",
        type=int,
        default=250,
        help="Number of output tokens to generate (default: 250)"
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="heterogeneous-prompts.csv",
        help="Output CSV file path (default: heterogeneous-prompts.csv)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="Start index for the prompts (default: 1)"
    )

    args = parser.parse_args()

    N_WORDS = args.workload_n_words
    M_WORDS = args.workload_m_words
    TOTAL_PROMPTS = args.total_prompts
    RATIO = args.ratio_n_to_m
    OUTPUT_TOKENS = args.output_tokens
    OUTPUT_FILE = args.output_csv
    SEED = args.seed
    START_INDEX = args.start_index

    # Calculate number of prompts for each type based on ratio
    n_prompts_count = int(TOTAL_PROMPTS * (RATIO / (RATIO + 1)))
    m_prompts_count = TOTAL_PROMPTS - n_prompts_count

    print(f"==== Generating heterogeneous workload:")
    print(f"==== Workload N: {N_WORDS} words, {n_prompts_count} prompts")
    print(f"==== Workload M: {M_WORDS} words, {m_prompts_count} prompts")
    print(f"==== Total prompts: {TOTAL_PROMPTS}")
    print(f"==== Output tokens per prompt: {OUTPUT_TOKENS}")
    print(f"==== Random seed: {SEED}")

    # Generate workload N prompts
    workload_n = []
    for i in range(n_prompts_count):
        rng = random.Random(SEED + i)
        prompt = make_prompt_with_index(i + START_INDEX, N_WORDS, rng)
        assert word_count(prompt) == N_WORDS, f"Workload N prompt {i} has {word_count(prompt)} words, expected {N_WORDS}"
        workload_n.append({
            "prompt": prompt,
            "output_tokens_count": OUTPUT_TOKENS,
        })

    # Generate workload M prompts
    workload_m = []
    for i in range(m_prompts_count):
        rng = random.Random(SEED + 10000 + i)  # Different seed range to ensure variety
        prompt = make_prompt_with_index(n_prompts_count + i + START_INDEX, M_WORDS, rng)
        assert word_count(prompt) == M_WORDS, f"Workload M prompt {i} has {word_count(prompt)} words, expected {M_WORDS}"
        workload_m.append({
            "prompt": prompt,
            "output_tokens_count": OUTPUT_TOKENS,
        })

    # Interleave the workloads
    combined = []

    # Follow the N:M ratio pattern (e.g., 3:1 -> N, N, N, M, N, N, N, M, ...)
    idx = 0
    n_idx = 0
    m_idx = 0
    while idx < TOTAL_PROMPTS:
        if idx % (RATIO + 1) == 0:
            combined.append(workload_m[m_idx])
            m_idx += 1
        else:
            combined.append(workload_n[n_idx])
            n_idx += 1
        idx += 1
    
    # Save to CSV
    df = pd.DataFrame(combined)

    # Reorder columns for better readability
    column_order = ["prompt", "output_tokens_count"]
    df = df[column_order]

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSuccessfully generated {len(combined)} prompts")
    print(f"Output saved to: {OUTPUT_FILE}")

    # Print summary statistics
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nSample prompts (first 100 chars):")
    print(f"Workload N: {workload_n[0]['prompt'][:100]}...")
    print(f"Workload M: {workload_m[0]['prompt'][:100]}...")


if __name__ == "__main__":
    main()
