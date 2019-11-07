from src.settings import postgres_password, postgres_database, postgres_host, postgres_user, postgres_schema
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


engine = create_engine(
    name_or_url=f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_database}",
    pool_pre_ping=True
)
Session = sessionmaker(bind=engine)
metadata = MetaData(engine, schema=postgres_schema)


@contextmanager
def session_scope():
    """from https://docs.sqlalchemy.org/en/13/orm/session_basics.html"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
