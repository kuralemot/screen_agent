from datetime import datetime
from pathlib import Path

import mss
from PIL import Image

from config import settings


def capture_screen() -> Image.Image:
    """Grabs the primary monitor as a PIL Image."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 0 is "all monitors"; 1 is the primary
        shot = sct.grab(monitor)
        return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")


def save_screenshot(image: Image.Image, directory: Path = None) -> Path:
    directory = directory or settings.screenshot_dir
    directory.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".png"
    path = directory / filename
    image.save(path)
    return path
