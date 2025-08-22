# SkryptPoetry AI

SkryptPoetry is a lightweight research environment that explores training and interaction with small textual datasets. It focuses on turning raw written material into a corpus of "skrypts" that guide future responses.

The project centers on `SkryptTrainer`, a minimal trainer that walks the repository and learns from markdown, text, JSON, and CSV files. A small SQLite log keeps track of file hashes so each document is processed only once.

Training can run asynchronously. When triggered, the trainer scans for new or modified files before performing any updates, allowing it to incorporate new information incrementally without costly reprocessing.

Interaction is handled by the `Symphony` agent. It receives messages, evaluates them against the dataset, and selects a fitting script based on resonance while logging entropy, perplexity, and resonance metrics.

Incoming messages are accumulated so that once they grow large enough, the text is fed back into the trainer for further learning. This loop lets the system gradually adapt to the conversation.

Retrieval‑augmented generation is provided through a simple retriever that compares a query to available documents and returns the most resonant snippet. This supports contextual replies rooted in the existing dataset.

Configuration files and dataset folders are kept intentionally small to emphasize clarity and quick experiments. The modular design allows swapping components or extending metrics without altering the core workflow.

A minimal model definition is included for future expansion, but the current implementation serves chiefly as an experimental playground for iterative training and logging on textual prompts.
