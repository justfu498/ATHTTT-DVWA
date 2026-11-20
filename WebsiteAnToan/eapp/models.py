from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from eapp import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    post_list = relationship('Post', backref='user', lazy=True)

    def __str__(self):
        return self.name

class Post(BaseModel):
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.title

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # u1 = User(name='Attacker', username='attacker', password=str(hashlib.md5('attacker123'.encode('utf-8')).hexdigest()))
        # u2 = User(name='Victim', username='victim', password=str(hashlib.md5('victim123'.encode('utf-8')).hexdigest()))
        #
        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.commit()