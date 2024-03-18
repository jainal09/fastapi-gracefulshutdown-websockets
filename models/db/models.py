from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

db = SessionLocal()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    message = Column(String)


class Flag(Base):
    __tablename__ = "flags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    allow_connections = Column(Boolean)
    UniqueConstraint("id", name="unique_id")
