# Standard library
import logging

# Internal modules
from app import app, teardown_application
from app.config import HeartbeatConfig
from app.service import emit_heartbeats


log = logging.getLogger(__file__)


def main() -> None:
    try:
        emit_heartbeats()
        app.start()
    except Exception as e:
        log.error(f'Application stopped: {str(e)}')
        teardown_application()


if __name__ == '__main__':
    main()
