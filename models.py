from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash

DB_URI = 'sqlite:///stuff.db'

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()


class User(Base):
    """
        Базовый пользовательский класс:
        Метод set_password - создает hash от пароля.
        Метод check_password поверяет правильность пароля.
        Метод to_dict преобразует экземпляр класса в словарь.
        Поле groupusers_id внешний ключ к классу GroupUsers.
        Поле groupusers добавлет класс GroupUsers в текущий класс
        по внешнему ключу.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), index=True, unique=True)
    firstname = Column(String(250))
    lastname = Column(String(250))
    groupusers_id = Column(Integer, ForeignKey("group_users.id"))
    groupusers = relationship("GroupUsers", backref='user')
    password_hash = Column(String(250))

    def __init__(self, username, firstname, lastname, groupusers_id):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.groupusers_id = groupusers_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        dict_user = {c.key: getattr(self, c.key)
                     for c in inspect(self).mapper.column_attrs}
        dict_group = {c.key: getattr(self, c.key).to_dict()
                      for c in inspect(self).mapper.relationships}
        dict_user.pop('password_hash')
        dict_user.pop('groupusers_id')
        return {**dict_user, **dict_group}


class GroupUsers(Base):
    """
        Ролевая модель:
            Метод to_dict преобразует экземпляр класса в словарь.
    """
    __tablename__ = 'group_users'
    id = Column(Integer, primary_key=True)
    groupname = Column(String(250))

    def __init__(self, groupname):
        self.groupname = groupname

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


Base.metadata.create_all(create_engine(DB_URI))
