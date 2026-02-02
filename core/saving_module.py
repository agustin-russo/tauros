import json
from core.routes import SAVES_DIR
from pathlib import Path


def save_config(config, filename):
    with open(SAVES_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    

def load_config(filename):
    filename = Path(filename)
    with open(filename, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config
