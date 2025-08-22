# SkryptPoetry AI

SkryptPoetry is a minimal experiment that turns natural language into symbolic "skrypts". The project began as a fork of a larger transformer repository but was trimmed to the essentials for rapid iteration and clarity.

SkryptTrainer sweeps the entire repository on each invocation, hashes eligible text files, and trains only on the ones it has not seen before. This approach keeps the model aligned with the latest project state without wasting computation on previously processed material.

SkryptLoger maintains a lightweight SQLite database that records every interaction and tracks which scripts and datasets have already contributed to training. Its tables provide persistent memory that prevents duplicate work and helps with later analysis of model behavior.

SkryptMetrics offers tiny yet informative statistics such as entropy, perplexity, resonance, and token charge. These metrics give quick feedback about the structure and familiarity of incoming text without requiring heavy models or external services.

The retrieval module, rag.py, performs resonance-based document search to surface the most relevant context from local datasets. It enables grounding of responses in project-specific knowledge by examining simple files under version control.

Symphony orchestrates the user experience. It selects unused scripts, logs metrics, triggers asynchronous training when conversation history grows, and generates replies by reusing the most resonant script for each message.

Traditional training utilities remain through model.py, train.py, and configurator.py, allowing deeper experimentation with transformer architectures and hyperparameters when needed. They coexist with the lighter training pipeline to support future expansion.

Project data lives in the datasets and tongue directories, which hold small Markdown corpora and script inventories. Adding or editing files in these folders—or anywhere in the repository—automatically feeds the trainer on the next request, keeping SkryptPoetry adaptable and ever-learning.
