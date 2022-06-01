"""These will be SQLAlchemy models, which are responsible for the models implemented on
our database."""
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey
)


# Database models that get mapped to tables

class Post(Base):
    # This will be the name thats mapped to the db
    __tablename__ = "posts"

    # Define the fields
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
    # Foreign key relationship with User table
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    # Create a relationship, must ref the class name to pull in
    # Docs: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # This represents a SQLAlchemy model which pydantic will model when you return schema.Post
    owner = relationship("User")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
    phone_number = Column(String())


class Vote(Base):

    __tablename__ = "votes"
    # Composite Primary key: Composed of (user_id, post_id)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
