from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base  # класс, от которого будем наследовать все таблицы БД
from sqlalchemy.orm import relationship

Base = declarative_base()


class GazzettaArticle(Base):
    __tablename__ = "GazzettaArticle"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    foreign_id = Column(String, nullable=False, unique=True)
    url = Column(String(2048), nullable=False, unique=True)
    title = Column(String(500), nullable=True, unique=False)
    image = Column(String(2048), nullable=True, unique=False)
    image_alt = Column(String(2048), nullable=True, unique=False)
    content = Column(String, nullable=False, unique=True)
    # crawled_url = Column(Integer, ForeignKey("CrawledUrls.id"), nullable=False)
    # crawled = relationship("CrawledUrls", backref="GazzettaArticle")


class Sentences(Base):
    __tablename__ = "Sentences"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    foreign_id = Column(String, ForeignKey("GazzettaArticle.foreign_id"), nullable=False, unique=False)
    foreign = relationship("GazzettaArticle", backref="Sentences")
    sentence_it = Column(String, nullable=False, unique=True)
    sentence_ru_auto = Column(String, nullable=True, unique=False)
    sentence_ru_valid = Column(String, nullable=True, unique=False)
