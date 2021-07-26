from datetime import datetime, timedelta

import jwt
from sqlalchemy import text, Column, String, Integer
from sqlalchemy.orm import Session
import bcrypt
import ulid

from app.service.errorhandler import ApplicationError, AuthorizationError
from domain import Base


private_key: bytes
with open('key/jwt_rsa.key') as key_file:
    private_key = key_file.read().encode('utf-8')


class User(Base):
    __tablename__ = 'user'
    ulid = Column(String, primary_key=True, default=ulid.new)
    login_id = Column(String, nullable=False)
    _user_pw = Column(String, nullable=False, name='user_pw')
    email = Column(String)
    refresh_token = Column(String)
    create_at = Column(Integer, server_default=text('UNIX_TIMESTAMP(NOW())'))
    update_at = Column(Integer, server_default=text('UNIX_TIMESTAMP(NOW())'), server_onupdate=text('UNIX_TIMESTAMP(NOW())'))
    user_pw = None
    confirm_pw = None

    def check_pw(self, login_pw):
        return bcrypt.checkpw(login_pw.encode('utf-8'), self._user_pw)

    def generate_password(self, user_pw):
        self._user_pw = bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())

    def update(self, **kwargs):
        if kwargs.get('confirm_pw'):
            if kwargs['user_pw'] == kwargs['confirm_pw']:
                self.generate_password(kwargs['user_pw'])
            else:
                raise AuthorizationError('Unmatched Confirm Password', code="4014")

        attr = self.__dir__()
        for k, v in kwargs.items():
            if k in attr:
                self.__setattr__(k, v)
            else:
                ApplicationError('attr error')

    def make_token(self, company_uuid: str):
        payload = {
            'uuid': self.uuid,
            'company_uuid': company_uuid,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }

        return jwt.encode(payload, private_key, algorithm="RS256")

    def make_refresh_token(self):
        payload = {'uuid': self.uuid,
                   'exp': datetime.utcnow() + timedelta(days=1)}
        self.refresh_token = jwt.encode(payload, private_key, algorithm="RS256")
        return self.refresh_token
