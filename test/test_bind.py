from src.bind import engine, session_scope


def test_connection():
    connection = engine.connect()
    connection.close()


def test_session_scope():
    with session_scope() as session:
        session.connection()
