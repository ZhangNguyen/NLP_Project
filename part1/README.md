# NLP Assignment 251 – Part I
Grammar construction, sentence generation, and parsing.

---

## 1. Environment Setup

This assignment run on Python 3.8

Install dependencies:

pip install -r requirements.txt

Note: The project uses only Python standard libraries, so no external packages are required.

---

## 2. How to Run

The main entrypoint of the project is:

python -m src.main --task <TASK_ID>

There are 3 tasks corresponding to the assignment sections.

---

### Task 2.1 – Export Grammar

Convert data/base_grammar.json to output/grammar.txt.

Run:

python -m src.main --task 2.1

Output file:
output/grammar.txt

---

### Task 2.2 – Generate Sentences

Generate sentences from the grammar.

Run:

python -m src.main --task 2.2 --max-sentences 10000

You may reduce the number for testing, for example:

python -m src.main --task 2.2 --max-sentences 100

Output file:
output/samples.txt

Each line contains one generated valid sentence.

---

### Task 2.3 – Parse Sentences

Parse each sentence inside input/sentences.txt.

Run:

python -m src.main --task 2.3

Output file:
output/parse-results.txt

Each line contains either:
- A full parse tree in bracket format, or
- "()" if the sentence cannot be parsed.

---

## 4. Input and Output Format

Input files:
1. data/base_grammar.json – Grammar rules in JSON.
2. input/sentences.txt – One sentence per line.

Output files:
1. grammar.txt
2. samples.txt
3. parse-results.txt

## 5. Author

Student: Nguyễn Minh Khang

ID Number: 2211452

Assignment: NLP Assignment 251 – Part I
