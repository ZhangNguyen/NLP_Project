# src/main.py
import argparse
from pathlib import Path
from .grammar import Grammar
from .generator import generate_sentences
from .parser import parse_sentence

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def task_2_1_export_grammar():
    ensure_output_dir()
    grammar = Grammar.from_json(DATA_DIR / "base_grammar.json")
    (OUTPUT_DIR / "grammar.txt").write_text(grammar.to_text(), encoding="utf-8")
    print("Wrote", OUTPUT_DIR / "grammar.txt")

def task_2_2_generate_samples(max_sentences: int = 10000):
    ensure_output_dir()
    grammar = Grammar.from_json(DATA_DIR / "base_grammar.json")
    sentences = generate_sentences(grammar, max_sentences=max_sentences)
    with (OUTPUT_DIR / "samples.txt").open("w", encoding="utf-8") as f:
        for s in sentences:
            f.write(s + "\n")
    print(f"Wrote {len(sentences)} sentences to", OUTPUT_DIR / "samples.txt")

def task_2_3_parse_sentences():
    ensure_output_dir()
    grammar = Grammar.from_json(DATA_DIR / "base_grammar.json")
    input_path = INPUT_DIR / "sentences.txt"
    output_path = OUTPUT_DIR / "parse-results.txt"
    lines = input_path.read_text(encoding="utf-8").splitlines()

    with output_path.open("w", encoding="utf-8") as f:
        for line in lines:
            if not line.strip():
                f.write("()\n")
                continue
            tree = parse_sentence(grammar, line)
            f.write(tree + "\n" if tree is not None else "()\n")

    print("Wrote parse results to", output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        choices=["2.1", "2.2", "2.3"],
        required=True,
        help="Which part of assignment to run"
    )
    parser.add_argument("--max-sentences", type=int, default=10000)
    args = parser.parse_args()

    if args.task == "2.1":
        task_2_1_export_grammar()
    elif args.task == "2.2":
        task_2_2_generate_samples(max_sentences=args.max_sentences)
    elif args.task == "2.3":
        task_2_3_parse_sentences()

if __name__ == "__main__":
    main()
