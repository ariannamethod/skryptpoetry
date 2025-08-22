## SkryptPoetry AI

SkryptPoetry is a lightweight transformer system that experiments with translating human language into the project's own symbolic "skrypt" representation.

The core model is defined in `model.py`, which implements a compact GPT-style architecture that can be trained or extended for language modeling tasks.

Training runs are managed by `SkryptTrainer`, which now scans the repository for new data on every request and avoids retraining files whose contents have not changed.

The `train.py` script coordinates end-to-end training workflows, loading configuration data, initializing models, and launching optimization routines.

Persistent metadata is handled by `skryptloger.py`, allowing the system to keep a record of processed files and track which inputs have contributed to the model.

Performance tracking utilities live in `skryptmetrics.py`, where simple metrics can be recorded to monitor progress and guide experiments.

Custom run configurations and dataset paths are defined in the `config` directory and can be managed programmatically through `configurator.py` to tailor experiments.

The repository is trimmed to only the components required for the neural network, making the codebase focused and easy to extend with additional functionality.
