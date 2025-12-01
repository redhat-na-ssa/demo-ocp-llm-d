import csv
import random
import textwrap
import argparse
import sys
import pandas as pd

# -------------------------------
# Helpers
# -------------------------------


def word_count(s: str) -> int:
    return len(s.split())


def make_base_prefix() -> str:
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


def make_base_continuation() -> str:
    base = """
    The continuation begins at the seam where the introduction hands off to deeper detail. It respects what is already
    known and adds substance without breaking tone. The team shifts from questions to practices, walking slowly through
    examples that a reader can visualize. First, they describe a library desk where a patron asks for a well-known guide.
    The librarian smiles because the guide sits in a public binder, already highlighted, already tabbed. Instead of
    rewriting the guide, the librarian says, "Turn to the section you need; the first pages are unchanged." The patron
    appreciates the small mercy. Next, the team describes a kitchen where cooks prepare a base stock every morning. When
    lunch begins, nobody remakes the stock; they build upon it with fresh ingredients. Finally, they describe a workshop
    where the same checklist starts each repair. Mechanics do not resent the checklist. They appreciate that it catches
    what routine can forget. These scenes are ordinary on purpose, because the goal is not spectacle but calm reliability.
    The continuation explains that a cache is a promise to remember shared beginnings so that attention can shift toward
    what is new. It then details safeguards: validation of the reused prefix, clear boundaries for where reuse stops, and
    transparent logs that help engineers see when routing decisions succeed or fail. It also discusses fairness, noting
    that cached work must be accurate, current, and appropriate for the request at hand. The text neither hurries nor
    stalls; it moves with the cadence of a thoughtful walkthrough, always returning to the reader with signposts that say,
    "Here is what changed," and, "Here is what stayed the same."
    """
    return textwrap.dedent(base).strip()


# Filler sentences used to pad out to exact word counts
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
    """Pad base_text with filler sentences until it reaches exactly target_words."""
    words = base_text.split()
    while len(words) < target_words:
        s = rng.choice(FILLER_SENTENCES)
        words.extend(s.split())
    trimmed = " ".join(words[:target_words])
    return trimmed


# -------------------------------
# Main generation
# -------------------------------


def parse_args(argv=None):
    """Parse command line arguments.

    Only --start-index was requested; a few extra optional args are provided as
    low-risk conveniences for smaller test runs or tuning without editing code.
    """
    p = argparse.ArgumentParser(
        description="Generate paired prefix + continuation prompts for cache-aware routing demos"
    )
    p.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="Starting pair id (inclusive). Defaults to 1.",
    )
    p.add_argument(
        "--num-pairs",
        type=int,
        default=5000,
        help="Number of pairs to generate beginning at start-index. Defaults to 5000.",
    )
    p.add_argument(
        "--target-prefix-words",
        type=int,
        default=5000,
        help="Word count for each prefix section. Defaults to 3000.",
    )
    p.add_argument(
        "--target-continuation-words",
        type=int,
        default=1000,
        help="Word count for each continuation section. Defaults to 3000.",
    )
    p.add_argument(
        "--output-prefix-csv",
        type=str,
        default="prefix-pairs.csv",
        help="Output CSV (side-by-side prefix + full prompt).",
    )
    p.add_argument(
        "--output-guidellm-csv",
        type=str,
        default="prefix-prompts.csv",
        help="Output CSV formatted for Guidellm consumption.",
    )
    p.add_argument(
        "--chunk-size",
        type=int,
        default=200,
        help="Number of prefix prompts before interleaving same number of continuation prompts (spacing). Defaults to 200.",
    )
    p.add_argument(
        "--output-tokens",
        type=int,
        default=250,
        help="Synthetic output token count annotation for each prompt row. Defaults to 250.",
    )
    args = p.parse_args(argv)
    if args.start_index < 1:
        p.error("--start-index must be >= 1")
    if args.num_pairs < 1:
        p.error("--num-pairs must be >= 1")
    if args.chunk_size < 1:
        p.error("--chunk-size must be >= 1")
    if args.output_tokens < 1:
        p.error("--output-tokens must be >= 1")
    return args


def main(argv=None):
    args = parse_args(argv)

    TARGET_PREFIX = args.target_prefix_words
    TARGET_CONT = args.target_continuation_words
    N_PAIRS = args.num_pairs
    START_INDEX = args.start_index
    output_path = args.output_prefix_csv

    prefix_base_template = make_base_prefix()
    continuation_base = make_base_continuation()

    # Precompute continuation text once (same continuation for all pairs)
    cont_rng = random.Random(9999)
    continuation_text = pad_to_word_count(continuation_base, TARGET_CONT, cont_rng)
    assert word_count(continuation_text) == TARGET_CONT, "Continuation not 3000 words"

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["pair_id", "prompt_1_prefix", "prompt_2_prefix_plus_continuation"]
        )
        end_index_exclusive = START_INDEX + N_PAIRS
        for i in range(START_INDEX, end_index_exclusive):
            # Slightly customize the prefix so each pair is different
            prefix_intro = (
                f"This is pair {i}, which demonstrates a long shared prefix that an engine "
                f"might cache and reuse across requests."
            )
            prefix_full_base = prefix_intro + " " + prefix_base_template

            rng = random.Random(i)  # deterministic variation per pair
            prefix_text = pad_to_word_count(prefix_full_base, TARGET_PREFIX, rng)

            full_prompt = prefix_text + " " + continuation_text

            # Quick sanity checks for first few pairs
            if i < START_INDEX + 3:
                assert word_count(prefix_text) == TARGET_PREFIX, (
                    f"Prefix length mismatch for pair {i}"
                )
                assert word_count(full_prompt) == TARGET_PREFIX + TARGET_CONT, (
                    f"Full prompt length mismatch for pair {i}"
                )

            writer.writerow([i, prefix_text, full_prompt])

    print(
        f"Done. Wrote {N_PAIRS} pairs (ids {START_INDEX}..{START_INDEX + N_PAIRS - 1}) to {output_path}. Formatting for guidellm..."
    )

    # Format for Guidellm.
    df = pd.read_csv(output_path)

    first_prompts = df["prompt_1_prefix"]
    second_prompts = df["prompt_2_prefix_plus_continuation"]
    first = first_prompts.tolist()
    second = second_prompts.tolist()

    # spacing between prefix and continuation blocks when interleaving
    CHUNK_SIZE = args.chunk_size
    combined = []
    for i in range(0, len(first), CHUNK_SIZE):
        combined.extend(first[i : i + CHUNK_SIZE])
        combined.extend(second[i : i + CHUNK_SIZE])

    # annotate with synthetic output tokens count
    OUTPUT_TOKENS = args.output_tokens
    OUTPUT_PATH = args.output_guidellm_csv
    save_df = pd.DataFrame(combined, columns=["prompt"])
    save_df["output_tokens_count"] = OUTPUT_TOKENS
    save_df.to_csv(OUTPUT_PATH, index=False)

    print(
        f"Done. Wrote {N_PAIRS} pairs (ids {START_INDEX}..{START_INDEX + N_PAIRS - 1}) to {OUTPUT_PATH}."
    )


if __name__ == "__main__":
    main(sys.argv[1:])
