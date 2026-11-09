from __future__ import annotations
from sqlalchemy import (Column,Integer,String,Boolean,ForeignKey,Text)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(
        String,
        unique=True,
        nullable=False)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False)

    hashed_password = Column(
        String,
        nullable=False)

    role = Column(
        String,
        default="user")

    is_active = Column(
        Boolean,
        default=True)

    #user can have many posts
    notes = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True)

    title = Column(
        String,
        nullable=False)

    content = Column(
        Text,
        nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False, index=True)

    owner = relationship(
        "User",
        back_populates="notes")