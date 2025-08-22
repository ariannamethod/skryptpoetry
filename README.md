## skryptpoetry ai
Transformer-type translator from human language to the language of skrypts.

### Dependencies

Runtime packages are pinned in `requirements.txt` and `arianna_linux/requirements.txt`. Development and testing tools live in `dev-requirements.txt`.

Skryptpoetry now centers on a lightweight training engine that continuously watches the repository for new knowledge. The trainer hashes eligible files and trains only on those it has not seen before, keeping the process efficient and adaptive to change.

Each request triggers a repository scan to ensure that fresh material is incorporated before any learning happens. This approach allows the model to stay synchronized with evolving datasets without manual intervention or redundant computation.

All interactions are archived through an integrated logging module. It records incoming messages, chosen scripts, and key metrics, providing a chronological record of the model's evolution and the context behind its outputs.

An accompanying metrics library exposes simple measures like entropy, perplexity, and resonance. These statistics offer quick insight into message complexity, prediction surprise, and textual alignment, enabling lightweight diagnostics of model behavior.

The Symphony agent orchestrates training, metrics, and retrieval. Upon receiving a message, it synchronizes the trainer, selects relevant script responses, and logs the resulting interaction, delivering a compact conversational loop.

Datasets stored under the `datasets` and `tongue` directories are automatically parsed whenever they change. By tracking file hashes, the trainer avoids duplicating work while still learning from any new or revised material in those locations.

Supported file types and ignored path segments are configurable through the ``allowed_extensions`` and ``excluded_parts`` parameters of :class:`SkryptTrainer`.

Retrieval of contextual passages is handled internally within Symphony. The agent scans available documents, measures their resonance with the query, and uses the best match to ground its response.

This modular architecture allows future expansion of the model, metrics, and training routines. With the repository constantly monitored, skryptpoetry remains ready to grow alongside new data and ideas.

The repository now includes an incremental training engine that scans designated directories, hashes file contents, and processes only unseen material, keeping the model up to date without redundant work.

Training runs are guarded by a thread lock and can be triggered asynchronously, letting background learning proceed while the system remains responsive to new inputs.

Every interaction and training event is persisted through a SQLite logging layer, creating a complete audit trail of messages, selected scripts, and computed metrics.

A compact metrics library exposes entropy, perplexity, resonance, and token charge, enabling rapid assessment of message complexity, surprise, alignment, and size.

The Symphony agent ties these components together, coordinating training, retrieval, metric calculation, and logging within a simple conversational loop.

Document retrieval employs a Jaccard-based resonance score to compare queries with potential sources and select the most relevant text for grounding responses.

Script selection encourages variety by marking used scripts in the database; when all scripts are exhausted, the system gracefully reuses entries to maintain functionality.

Dataset and script directories are continuously watched for changes, ensuring that new or updated files are incorporated into future training passes.

Concurrency tests confirm that multiple threads invoking training simultaneously still result in a single pass per file, demonstrating correct locking and database usage.

The modular design leaves room for future expansion of models, metrics, and training strategies while keeping the current implementation lightweight and easy to maintain.
