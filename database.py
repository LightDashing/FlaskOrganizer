from sqlalchemy import Column, INTEGER, Text, ForeignKey, VARCHAR, DATE, Boolean
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import Session, relationship
import datetime
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    username = Column(VARCHAR(30), unique=True, nullable=False)
    email = Column(VARCHAR(30), unique=True, nullable=False)
    password = Column(VARCHAR(512), nullable=False)
    registration_date = Column(Text, nullable=False, default=datetime.date.today().isoformat())

    user_tasks = relationship("Task")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('users.id'), nullable=False)
    title = Column(VARCHAR(30), nullable=False)
    description = Column(Text)
    status = Column(Boolean, nullable=False, default=False)
    start_date = Column(Text, nullable=False, default=datetime.date.today().isoformat())
    end_date = Column(Text)

    user = relationship(User)

class DBWork:

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:***REMOVED***@localhost/postgres', echo=True)
        self.session = Session(bind=self.engine)

    def close(self):
        self.session.close()

    def user_add(self, username, email, password):
        self.session.add(User(username=username, email=email, password=password))
        try:
            self.session.commit()
            return True
        except (UniqueViolation, IntegrityError):
            self.close()
            return False

    def commit(self):
        self.session.commit()


    def user_login(self, email, password):
        user = self.session.query(User).filter(User.email==email, User.password==password).all()
        if user:
            return True
        else:
            return False

    def get_user_nickname(self, email):
        user = self.session.query(User).filter(User.email==email).first()
        if user:
            return user[0].username
        else:
            return False

    def task_add(self, title, description, deadline, user_id):
        self.session.add(Task(title=title, description=description, end_date=deadline, user_id=user_id))
        self.commit()

    def get_user_data(self, username):
        user = self.session.query(User).filter(User.username==username).first()
        return user
