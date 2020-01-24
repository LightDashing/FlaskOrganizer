from sqlalchemy import Column, INTEGER, Text, ForeignKey, VARCHAR, DATE, Boolean
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import Session, relationship
import datetime
import sqlalchemy.ext.IntegrityError

engine = create_engine('postgresql://postgres:***REMOVED***@localhost/postgres', echo=True)
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
        self.session = Session(bind=engine)

    def close(self):
        self.session.close()

    def user_add(self, username, email, password):
        self.session.add(User(username=username, email=email, password=password))

    def commit(self):
        self.session.commit()


Base.metadata.create_all(engine)
session = Session(bind=engine)
#session.add(User(username='LightDashing', email='chugunnic@gmal.com', password='rjombabomba'))
#session.commit()
response = session.query(User).all()
print(response[0].username)
session.close()