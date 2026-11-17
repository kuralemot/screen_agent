import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")


def _bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    vllm_base_url: str = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
    vllm_api_key: str = os.getenv("VLLM_API_KEY", "not-needed")
    vllm_model: str = os.getenv("VLLM_MODEL", "LiquidAI/LFM3-VL")
    stub_vlm: bool = _bool("STUB_VLM", True)

    capture_interval_seconds: float = float(os.getenv("CAPTURE_INTERVAL_SECONDS", "30"))
    save_screenshots: bool = _bool("SAVE_SCREENSHOTS", True)
    screenshot_dir: Path = ROOT_DIR / os.getenv("SCREENSHOT_DIR", "data/screenshots")

    chroma_dir: Path = ROOT_DIR / os.getenv("CHROMA_DIR", "data/chroma_db")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "screen_observations")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


settings = Settings()
