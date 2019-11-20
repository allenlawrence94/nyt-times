from src.model import Time, Player
from .fixtures import db, users
from src.bind import session_scope
import datetime as dt
from dateutil.tz import gettz
from sqlalchemy.exc import IntegrityError
import pytest


def test_setup(db):
    with session_scope() as sesh:
        assert sesh.execute(
            "SELECT EXISTS ( "
            "SELECT 1 "
            "FROM   information_schema.tables "
            f"WHERE  table_name = '{Time.__tablename__}' "
            ");"
        ).fetchone() == (1,)


def test_time(users):
    with session_scope() as sesh:
        time = Time(
            player_id=1,
            time=34.5,
            game='easy4'
        )
        assert dt.datetime.now(tz=gettz('America/New_York')).date() == time.date
        sesh.add(time)

    with session_scope() as sesh:
        time = sesh.query(Time).one()
        assert time.player_id == 1
        assert time.time == 34.5
        assert time.game == 'easy4'

    with pytest.raises(IntegrityError):
        with session_scope() as sesh:
            time = Time(
                player_id=1,
                time=25,
                game='easy4'
            )
            sesh.add(time)


def test_player(users):
    with session_scope() as sesh:
        players = sesh.query(Player).all()
        assert players[0].id == 1
        assert players[0].name == 'foo'
        assert players[1].id == 2
        assert players[1].name == 'bar'

    with pytest.raises(IntegrityError):
        with session_scope() as sesh:
            sesh.add(Player('foo'))
