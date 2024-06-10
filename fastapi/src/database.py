from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mariadb+mariadbconnector://user:password@mariadb:3306/database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    val = Column(String)


def get_message_by_id(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
