
from sqlalchemy import Column, Text
from .base import Base, BaseColumns
from flask_security import RoleMixin


class Message(Base, BaseColumns, RoleMixin):
    __tablename__ = "messages"

    message = Column(Text, server_default='')


