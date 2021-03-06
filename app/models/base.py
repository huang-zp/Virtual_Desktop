# coding: utf-8
from sqlalchemy import Column, BigInteger, func, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseColumns:
    id = Column(BigInteger(), primary_key=True, nullable=False,
                autoincrement=True, unique=True)
    create_time = Column(TIMESTAMP, server_default=func.now(), index=True)
    update_time = Column(TIMESTAMP, server_default=func.now(), index=True)

