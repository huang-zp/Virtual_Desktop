from sqlalchemy import Column
from sqlalchemy import Integer
from .base import Base, BaseColumns


class User_Desktop(Base, BaseColumns):
    __tablename__ = "user_desktops"

    user_id = Column(Integer(), server_default='0')
    desktop_id = Column(Integer(), server_default='0')









