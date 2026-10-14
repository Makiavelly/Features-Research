"""Same GloVe encoder as upstream, using the verified local model snapshot."""
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer


class GloveTextEmbedding:
    def __init__(self, device=None):
        root = Path(__file__).resolve().parents[1]
        self.model_path = root / "data/models/glove"
        self.device = device
        self.model = None

    def __call__(self, sentences):
        if self.model is None:
            self.model = SentenceTransformer(str(self.model_path), device=self.device)
        cleaned = ["" if value is None or isinstance(value, float) and value != value else str(value) for value in sentences]
        return self.model.encode(cleaned, convert_to_tensor=True)
