import logging
import pytest


@pytest.fixture(autouse=True)
def configure_logging_for_tests():
    logger = logging.getLogger("redirect_service")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    yield
