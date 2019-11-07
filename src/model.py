from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, UniqueConstraint, Date, Float
from alembic.config import Config as AlembicConfig
import alembic.command as alc


Base = declarative_base()


class Times(Base):

    __tablename__ = 'times'
    __table_args__ = (
        UniqueConstraint('date', 'game', 'player'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(Date, server_default=func.current_date(), nullable=False)
    game = Column(String, nullable=False)
    player = Column(String, nullable=False)
    time = Column(Float, nullable=False)

    def __init__(self, player, time, game='nyt-mini'):
        self.player = player
        self.time = time
        self.game = game

    @validates('time')
    def validates_time(self, key, time):
        if time <= 0.:
            raise ValueError(f'time must be greater than 0.')
        return time


def setup(revision='head'):
    alc.upgrade(AlembicConfig('alembic.ini'), revision)


def teardown():
    alc.downgrade(AlembicConfig('alembic.ini'), 'base')
