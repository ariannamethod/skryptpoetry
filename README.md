## skryptpoetry ai
Transformer-type translator from human language to the language of skrypts.

Skryptpoetry now centers on a lightweight training engine that continuously watches the repository for new knowledge. The trainer hashes eligible files and trains only on those it has not seen before, keeping the process efficient and adaptive to change.

Each request triggers a repository scan to ensure that fresh material is incorporated before any learning happens. This approach allows the model to stay synchronized with evolving datasets without manual intervention or redundant computation.

All interactions are archived through an integrated logging module. It records incoming messages, chosen scripts, and key metrics, providing a chronological record of the model's evolution and the context behind its outputs.

An accompanying metrics library exposes simple measures like entropy, perplexity, and resonance. These statistics offer quick insight into message complexity, prediction surprise, and textual alignment, enabling lightweight diagnostics of model behavior.

The Symphony agent orchestrates training, metrics, and retrieval. Upon receiving a message, it synchronizes the trainer, selects relevant script responses, and logs the resulting interaction, delivering a compact conversational loop.

Datasets stored under the `datasets` and `tongue` directories are automatically parsed whenever they change. By tracking file hashes, the trainer avoids duplicating work while still learning from any new or revised material in those locations.

Retrieval of contextual passages is handled internally within Symphony. The agent scans available documents, measures their resonance with the query, and uses the best match to ground its response.

This modular architecture allows future expansion of the model, metrics, and training routines. With the repository constantly monitored, skryptpoetry remains ready to grow alongside new data and ideas.
