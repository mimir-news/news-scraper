# Standard library
import logging
import time
from pathlib import Path
from threading import Thread

# Internal modules
from app.config import HealthCheckConfig
from .mq_clients import MQConnectionChecker


_log = logging.getLogger(__file__)


def emit_heartbeats(checker: MQConnectionChecker) -> None:
    """Sets up and runs heartbeat emissions in a background tread."""
    config = HealthCheckConfig()
    t = Thread(
        target=_run_heartbeats_in_background,
        args=(config, checker, ))
    t.setDaemon(True)
    t.start()


def _run_heartbeats_in_background(config: HealthCheckConfig, checker: MQConnectionChecker) -> None:
    """Touch a file to inform healthcheckers that the service is running.

    :param filepath: Full path to the file to touch.
    :param interval_seconds: Interval of emiting lifesigns in seconds.
    """
    while True:
        if checker.is_connected(config.MQ_HEALTH_TARGET):
            Path(config.FILENAME).touch()
        else:
            _log.warn("MQ is not connected")
        time.sleep(config.INTERVAL)
