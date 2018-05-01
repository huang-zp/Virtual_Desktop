
from sqlalchemy import Column, Text
from sqlalchemy import String
from .base import Base, BaseColumns
from flask_security import RoleMixin


class Desktop(Base, BaseColumns, RoleMixin):
    __tablename__ = "desktops"

    name = Column(String(50), server_default='')
    description = Column(Text, server_default='')
    server = Column(String(50), server_default='')
    port = Column(String(50), server_default='')
    system = Column(String(50), server_default='')
    user = Column(String(50), server_default='')
    server_password = Column(String(50), server_default='')

