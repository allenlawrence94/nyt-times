import pytest
from src.model import setup, teardown
from src.bind import engine


@pytest.fixture(scope='function')
def db():
    try:
        setup()
        yield
    finally:
        engine.dispose()
        teardown()
