import time

import capture
import rag_store
import vlm_client
from config import settings


def observe_once() -> dict:
    image = capture.capture_screen()
    screenshot_path = None
    if settings.save_screenshots:
        screenshot_path = capture.save_screenshot(image)

    description = vlm_client.describe_image(image)
    obs_id = rag_store.add_observation(description, screenshot_path)

    return {"id": obs_id, "description": description, "screenshot_path": screenshot_path}


def run_loop():
    print(
        f"Starting screen observation loop (every {settings.capture_interval_seconds}s). "
        f"STUB_VLM={settings.stub_vlm}. Ctrl+C to stop."
    )
    try:
        while True:
            obs = observe_once()
            print(f"[{obs['id'][:8]}] {obs['description']}")
            time.sleep(settings.capture_interval_seconds)
    except KeyboardInterrupt:
        print("\nStopped.")
