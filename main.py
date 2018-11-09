# Standard library
import logging

# Internal modules
from app import app, teardown_application


log = logging.getLogger(__file__)


def main() -> None:
    try:
        app.start()
    except Exception as e:
        log.error(f'Application stopped: {str(e)}')
        teardown_application()


if __name__ == '__main__':
    main()
