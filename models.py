from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    persona = relationship("Persona", back_populates="user", uselist=False)
    messages = relationship("Message", back_populates="user")
    memories = relationship("Memory", back_populates="user")


class Persona(Base):
    __tablename__ = "persona"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    personality = Column(Text, nullable=False)
    tone = Column(String, nullable=False)
    likes = Column(Text)
    dislikes = Column(Text)
    
    user = relationship("User", back_populates="persona")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender = Column(String, nullable=False)  # 'user' or 'ai'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="messages")


class Memory(Base):
    __tablename__ = "memory"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)
    
    user = relationship("User", back_populates="memories")
