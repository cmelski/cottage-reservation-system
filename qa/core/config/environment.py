from pathlib import Path
from dotenv import load_dotenv


def load_environment(env_name):
    root = Path(__file__).resolve().parents[3]
    env_path = root / f"{env_name}.env"

    load_dotenv(env_path, override=True)
