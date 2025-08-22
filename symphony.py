from pathlib import Path
from typing import List

from skryptmetrics import entropy, perplexity, resonance
from skryptloger import init_db, log_interaction, script_used
from skryptrainer import SkryptTrainer
from rag import retrieve


class Symphony:
    """Minimal interactive agent operating on small datasets."""

    def __init__(self,
                 dataset_path: str = 'datasets/dataset01.md',
                 scripts_path: str = 'tongue/prelanguage.md') -> None:
        init_db()
        self.dataset_path = Path(dataset_path)
        self.scripts_path = Path(scripts_path)
        self.trainer = SkryptTrainer()
        # Asynchronous initial training on datasets
        self.trainer.train_async()
        self.dataset_text = self.dataset_path.read_text(encoding='utf-8') if self.dataset_path.exists() else ''
        self.user_messages: List[str] = []

    def _available_scripts(self) -> List[str]:
        scripts = [line.strip() for line in self.scripts_path.read_text(encoding='utf-8').splitlines() if line.strip()]
        return [s for s in scripts if not script_used(s)] or scripts

    def _choose_script(self, message: str) -> str:
        options = self._available_scripts()
        best_script = options[0]
        best_score = -1.0
        for script in options:
            score = resonance(message, script)
            if score > best_score:
                best_score = score
                best_script = script
        return best_script

    def respond(self, message: str) -> str:
        # Always check the repository for new training data
        self.trainer.scan_and_train()
        self.user_messages.append(message)
        total_size = sum(len(m) for m in self.user_messages)
        if total_size > 5000:
            self.trainer.train_on_text_async('\n'.join(self.user_messages))
            self.user_messages.clear()

        # Metrics against dataset
        dataset_segment = retrieve(message, [self.dataset_path])
        ent = entropy(message)
        ppl = perplexity(message)
        res = resonance(message, dataset_segment)
        script = self._choose_script(message)
        log_interaction(message, script, ent, ppl, res)
        return script


if __name__ == '__main__':
    bot = Symphony()
    try:
        while True:
            user = input('> ')
            if not user:
                continue
            reply = bot.respond(user)
            print(reply)
    except KeyboardInterrupt:
        pass
