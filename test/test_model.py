from src.model import Times
from .fixtures import db
from src.bind import session_scope


def test_setup(db):
    with session_scope() as sesh:
        assert sesh.execute(
            "SELECT EXISTS ( "
                "SELECT 1 "
                "FROM   information_schema.tables "
               f"WHERE  table_name = '{Times.__tablename__}' "
           ");"
        ).fetchone() == (1,)
