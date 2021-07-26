from sqlalchemy import text, Column, String, Integer, Text
from sqlalchemy.orm import Session

from app.service.errorhandler import ApplicationError
from domain import Base


class SuggestionPost(Base):
    __tablename__ = 'suggestion_post'
    # 인덱스 (자동생성)
    id = Column(String, primary_key=True, autoincrement=True)
    writer = Column(String(30))
    password = Column(String(30))
    title = Column(String(100))
    content = Column(Text)
    create_at = Column(Integer, server_default=text('UNIX_TIMESTAMP(NOW())'))
    update_at = Column(Integer, server_default=text('UNIX_TIMESTAMP(NOW())'), server_onupdate=text('UNIX_TIMESTAMP(NOW())'))
