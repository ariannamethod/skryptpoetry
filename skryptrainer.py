import hashlib
import threading
from pathlib import Path
from typing import Iterable

from skryptloger import init_db, log_trained_file, was_trained

ALLOWED_EXTENSIONS = {".md", ".txt", ".json", ".csv"}


class SkryptTrainer:
    """Lightweight trainer that scans directories and avoids retraining."""

    def __init__(
        self,
        base_path: str | Path | None = None,
        datasets: Iterable[str] = ("datasets", "tongue"),
    ):
        self.base_path = Path(base_path) if base_path else Path(__file__).resolve().parent
        # include repository root and optional datasets
        self.dirs = [self.base_path] + [self.base_path / p for p in datasets]
        init_db()

    def _file_hash(self, path: Path) -> str:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            h.update(f.read())
        return h.hexdigest()

    def _eligible_files(self) -> Iterable[Path]:
        for directory in self.dirs:
            if not directory.exists():
                continue
            for file in directory.rglob("*"):
                if ".git" in file.parts:
                    continue
                if file.is_file() and file.suffix.lower() in ALLOWED_EXTENSIONS:
                    yield file

    def _train_file(self, path: Path) -> None:
        """Placeholder for real training routine."""
        # In real life, training data would be fed to the model here.
        pass

    def scan_and_train(self) -> None:
        for file in self._eligible_files():
            sha = self._file_hash(file)
            if not was_trained(file, sha):
                self._train_file(file)
                log_trained_file(file, sha)

    def train_async(self) -> None:
        threading.Thread(target=self.scan_and_train, daemon=True).start()

    def train_on_text(self, text: str) -> None:
        """Placeholder training on raw text."""
        # Always refresh repository knowledge before training on new text
        self.scan_and_train()
        # In real life, training data would be fed to the model here.
        pass

    def train_on_text_async(self, text: str) -> None:
        threading.Thread(target=self.train_on_text, args=(text,), daemon=True).start()
