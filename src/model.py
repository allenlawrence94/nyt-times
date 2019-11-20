from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, UniqueConstraint, Date, DateTime, Float, ForeignKey, MetaData
from alembic.config import Config as AlembicConfig
import alembic.command as alc
from .settings import postgres_schema
from .constants import games, nyt_tz
import datetime as dt


Base = declarative_base(metadata=MetaData(schema=postgres_schema))


class InvalidParameter(ValueError):
    pass


class Time(Base):

    __tablename__ = 'time'
    __table_args__ = (
        UniqueConstraint('date', 'game', 'player_id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(Date, nullable=False)
    datetime = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    game = Column(String, nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'))
    time = Column(Float, nullable=False)

    def __init__(self, player_id, time, game):
        self.player_id = player_id
        self.time = time
        self.game = game
        self.date = dt.datetime.now(nyt_tz).date()

    @validates('time')
    def validates_time(self, key, time):
        if time <= 0.:
            raise InvalidParameter(f'time must be greater than 0., got {time}')
        return time

    @validates('game')
    def validates_game(self, key, game):
        if game not in games:
            raise InvalidParameter(f'game must be in {games}, got {game}')
        return game


class Player(Base):

    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name


def setup(revision='head'):
    alc.upgrade(AlembicConfig('alembic.ini'), revision)


def teardown():
    alc.downgrade(AlembicConfig('alembic.ini'), 'base')
