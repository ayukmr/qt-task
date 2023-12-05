import os, binascii

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# create engine
Base = declarative_base()
engine = create_engine('sqlite:///cards.db')

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Cards database
class Cards(Base):
    __tablename__ = 'Cards'

    # card id
    id = Column(String, primary_key=True, default=lambda: binascii.b2a_hex(os.urandom(16)).decode('utf-8'))

    # card title
    title = Column(String)

    # card difficulty
    difficulty = Column(Integer)

    # card description
    description = Column(String)

# insert card
def insert(title, difficulty, description):
    new_row = Cards(title=title, difficulty=difficulty, description=description)

    session.add(new_row)
    session.commit()

# update card
def update(row_id, title, difficulty, description):
    row = session.query(Cards).filter(Cards.id == row_id).first()

    # update values
    row.title       = title
    row.difficulty  = difficulty
    row.description = description

    session.commit()

# delete card
def delete(row_id):
    row = session.query(Cards).filter(Cards.id == row_id).first()

    session.delete(row)
    session.commit()

# all cards
def all():
    rows = session.query(Cards).all()
    return [{'id': row.id, 'title': row.title, 'difficulty': row.difficulty, 'description': row.description} for row in rows]

# create all
Base.metadata.create_all(engine)