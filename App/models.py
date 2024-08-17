from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
