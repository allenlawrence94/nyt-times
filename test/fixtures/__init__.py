import pytest
from src.model import setup, teardown, Player
from src.bind import engine, session_scope


@pytest.fixture(scope='function')
def db():
    try:
        setup()
        yield
    finally:
        engine.dispose()
        teardown()


@pytest.fixture(scope='function')
def users(db):
    with session_scope() as sesh:
        sesh.add(Player(name='foo'))
        sesh.add(Player(name='bar'))
    yield
