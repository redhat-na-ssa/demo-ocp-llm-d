import argparse
import csv
import random
import sys
import textwrap

# Approximate tokens-per-word ratio for English prose
TOKENS_PER_WORD = 1.3

# -------------------------------
# Helpers
# -------------------------------


def make_base_text() -> str:
    base = """
    The project began as a simple curiosity about how people share context. A small team looked at the way
    long prompts flowed through a system and noticed that many early sentences said the same thing again and again.
    They wrote notes about repetition, alignment, and the invisible friction that appears when a model must read
    familiar paragraphs before it reaches anything new. The team proposed a study that would demonstrate why
    prefix-aware routing matters, not as a trick of engineering, but as a quiet improvement in everyday experience.
    They chose to write in plain and sturdy English so that anyone could skim the pages and still understand the point.
    The introduction framed a question: if a service can recognize an already-seen beginning, can it spare effort, time,
    and energy by reusing what it already knows? The group suspected that the answer was yes, but they also believed
    that the demonstration should be gentle, measurable, and honest about tradeoffs. They decided to build a dataset
    of paired prompts where the second part meaningfully continues the first. Each pair would resemble a calm essay,
    with paragraphs that move at an even pace, never rushing, never leaning on jargon, never demanding specialist knowledge.
    They wrote examples about communities, tools, learning, and the patient rhythms of maintenance. They gave names to
    recurring ideas: shared context, stable ground, incremental novelty, careful transitions, and endings that feel earned.
    Paragraph by paragraph, they drew a path across familiar terrain, noting how predictability can be a gift. A reader
    who recognizes the early sections can focus attention on the fresh material that follows. An engine that recognizes
    the early sections can reuse cached work and save effort for what truly changes. The team wanted prose that was
    specific enough to feel real while remaining broadly applicable. They spoke about kitchens, libraries, workshops,
    classrooms, neighborhoods, and gardens. They emphasized the kindness of clear signposts, steady tempo, and
    smooth handoffs between sections. They also noted risks: if a system guesses wrong about a prefix, it can add
    confusion rather than clarity. So each example would be constructed with careful seams, obvious transitions,
    and natural cues that signal continuity. In this way, the dataset would be useful for demonstration, inspection,
    and repeatable measurement. The group hoped that anyone who read a sample would see the intuitive appeal of
    cache-aware routing long before they looked at charts or timing numbers. They trusted that the writing itself
    could serve as evidence, because good structure wastes nothing and gives attention back to the reader.
    """
    return textwrap.dedent(base).strip()


FILLER_SENTENCES = [
    "This sentence maintains the calm tempo and reinforces the central thread of reuse and careful change.",
    "The writing keeps an even stride, trading spectacle for clarity and quiet confidence.",
    "Each paragraph tries to waste nothing, offering small details that feel steady rather than dramatic.",
    "Readers should sense continuity without needing to decipher jargon or decode sudden leaps in logic.",
    "The examples remain ordinary on purpose, because ordinary tasks reveal the value of dependable structure.",
    "At every turn the prose names what is shared first, and only then points gently to what is new.",
    "When familiar ground appears, the text acknowledges it openly and moves ahead without lingering.",
    "A measured voice invites trust, and trust lets the reader notice improvements that might otherwise hide.",
    "The goal is transparency, not surprise; the lesson is patient rather than performative.",
    "By echoing known phrases, the passage guides attention toward the moment where novelty begins.",
    "The cadence is the same as before: simple words, clear transitions, and respect for the reader's time.",
    "Nothing essential is rushed; nothing trivial is allowed to sprawl.",
    "Where a claim is made, an example follows; where an example appears, a reason accompanies it.",
    "Structure becomes a kind of kindness, returning minutes to people who have many tasks to finish.",
    "The text keeps circling back to the theme that good routing honors both memory and change.",
    "If a seam is visible, it is visible on purpose, so that the reader can step across without stumbling.",
    "Practicality outweighs novelty here; the point is usefulness that lasts beyond the page.",
    "Even the metaphors are familiar, chosen to welcome rather than to impress.",
    "The passage stays specific enough to be testable and general enough to travel.",
    "Small repetitions are not mistakes; they are signposts that help readers track the path.",
    "The narrative knows where it came from and declares where it is going.",
    "Every figure of speech earns its place by serving the explanation rather than decorating it.",
    "When doubt appears, the text slows down and states assumptions in plain view.",
    "The argument prefers daylight to mystery, procedure to flourish.",
    "Taken together, these sentences model the very economy the system aims to provide.",
]


def pad_to_word_count(base_text: str, target_words: int, rng: random.Random) -> str:
    words = base_text.split()
    while len(words) < target_words:
        words.extend(rng.choice(FILLER_SENTENCES).split())
    return " ".join(words[:target_words])


# -------------------------------
# Main
# -------------------------------


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Generate repeated prompts sized to fill a target KV-cache occupancy"
    )
    p.add_argument(
        "--kv-cache-size",
        type=int,
        required=True,
        help="KV-cache capacity per replica, in tokens.",
    )
    p.add_argument(
        "--num-replicas",
        type=int,
        required=True,
        help="Number of serving replicas.",
    )
    p.add_argument(
        "--prompt-size",
        type=int,
        required=True,
        help="Target size of each prompt, in tokens.",
    )
    p.add_argument(
        "--num-pairs",
        type=int,
        required=True,
        help="Number of times each unique prompt is repeated.",
    )
    p.add_argument(
        "--repeat-gap",
        type=int,
        default=10,
        help="Number of other prompts between consecutive repetitions of the same prompt. Defaults to 10.",
    )
    p.add_argument(
        "--output-tokens",
        type=int,
        default=250,
        help="Synthetic output-token-count annotation per row. Defaults to 250.",
    )
    p.add_argument(
        "--output",
        type=str,
        default="prompts.csv",
        help="Output CSV path. Defaults to prompts.csv.",
    )
    args = p.parse_args(argv)
    if args.kv_cache_size < 1:
        p.error("--kv-cache-size must be >= 1")
    if args.num_replicas < 1:
        p.error("--num-replicas must be >= 1")
    if args.prompt_size < 1:
        p.error("--prompt-size must be >= 1")
    if args.num_pairs < 1:
        p.error("--num-pairs must be >= 1")
    if args.repeat_gap < 0:
        p.error("--repeat-gap must be >= 0")
    if args.output_tokens < 1:
        p.error("--output-tokens must be >= 1")
    return args


def main(argv=None):
    args = parse_args(argv)

    # --- capacity math (80% fill target) ---
    tokens_at_80pct = int(args.kv_cache_size * 0.8)
    unique_per_replica = tokens_at_80pct // args.prompt_size
    if unique_per_replica < 1:
        sys.exit(
            f"Error: prompt size ({args.prompt_size} tokens) exceeds 80% of "
            f"KV-cache ({tokens_at_80pct} tokens). Cannot fit even one prompt."
        )
    total_unique = unique_per_replica * args.num_replicas

    # Convert token target to approximate word target
    target_words = max(1, int(args.prompt_size / TOKENS_PER_WORD))

    print(
        f"KV cache 80%: {tokens_at_80pct} tokens/replica  ->  "
        f"{unique_per_replica} unique prompts/replica  x  {args.num_replicas} replicas  =  "
        f"{total_unique} unique prompts total"
    )
    print(f"Target prompt length: ~{target_words} words (~{args.prompt_size} tokens)")

    # --- generate unique prompts ---
    base = make_base_text()
    prompts = []
    for i in range(1, total_unique + 1):
        intro = (
            f"This is prompt {i}, which demonstrates a long shared prefix that an engine "
            f"might cache and reuse across requests."
        )
        rng = random.Random(i)
        prompt = pad_to_word_count(intro + " " + base, target_words, rng)
        prompts.append(prompt)

    # --- repeat with controlled gap ---
    if args.num_pairs > 1:
        chunk_size = max(1, args.repeat_gap + 1)
        expanded = []
        for i in range(0, len(prompts), chunk_size):
            chunk = prompts[i : i + chunk_size]
            for _ in range(args.num_pairs):
                expanded.extend(chunk)
        prompts = expanded

    # --- write guidellm-compatible CSV ---
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt", "output_tokens_count"])
        for prompt in prompts:
            writer.writerow([prompt, args.output_tokens])

    print(
        f"Done. Wrote {len(prompts)} rows "
        f"({total_unique} unique x {args.num_pairs} repetitions) to {args.output}."
    )


if __name__ == "__main__":
    main(sys.argv[1:])
