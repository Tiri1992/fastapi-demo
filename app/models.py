"""Define our models as python objs."""

from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP
)


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
