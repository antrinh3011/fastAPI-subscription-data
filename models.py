# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Keyword(Base):
    __tablename__ = 'keyword'

    keyword_id = Column(BigInteger, primary_key=True)
    keyword_name = Column(String(255), unique=True)


class KeywordSearchVolume(Base):
    __tablename__ = 'keyword_search_volume'

    keyword_id = Column(ForeignKey('keyword.keyword_id'), primary_key=True, nullable=False)
    created_datetime = Column(DateTime, primary_key=True, nullable=False)
    search_volume = Column(BigInteger)

    keyword = relationship('Keyword')


class UserSubscription(Base):
    __tablename__ = 'user_subscription'

    user_id = Column(BigInteger, primary_key=True, nullable=False)
    keyword_id = Column(ForeignKey('keyword.keyword_id'), primary_key=True, nullable=False, index=True)
    subscription_start = Column(DateTime)
    subscription_end = Column(DateTime)
    timing = Column(String(45))

    keyword = relationship('Keyword')
