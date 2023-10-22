from email.policy import default
import enum
from typing import Union
import uuid
from fastapi import Security

from sqlalchemy import (Boolean, Column, ForeignKey,
                        String, Table, Enum, DateTime,
                        Text, Integer, Float,event
                        )
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.event import listen
from sqlalchemy.ext.associationproxy import association_proxy

from ..database.database import Base, SessionLocal


class File(Base):
    __tablename__ = "files"

    p_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )