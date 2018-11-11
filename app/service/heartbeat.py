# Standard library
import time
from pathlib import Path
from threading import Thread

# Internal modules
from app.config import HeartbeatConfig


def emit_heartbeats() -> None:
    """Sets up and runs heartbeat emissions in a background tread."""
    config = HeartbeatConfig()
    t = Thread(
        target=_run_heartbeats_in_background,
        args=(config.FILE, config.INTERVAL, ))
    t.setDaemon(True)
    t.start()


def _run_heartbeats_in_background(filepath: str, interval_seconds: int) -> None:
    """Touch a file to inform healthcheckers that the service is running.

    :param filepath: Full path to the file to touch.
    :param interval_seconds: Interval of emiting lifesigns in seconds.
    """
    while True:
        Path(filepath).touch()
        time.sleep(interval_seconds)
