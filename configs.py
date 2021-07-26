import os
from functools import lru_cache
from pathlib import Path

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    app create 시 저장되는 설정들
    _로 시작하면 설정에 포함시키지 않는다.
    소문자 : fast api 기본 설정
    대문자 : 커스텀 설정
    """
    title = "EXERCIDER"
    description = "EXERCIDER SERVER"
    version = "0.1.0"
    openapi_tags = [
        {
            "name": "public",
            "description": "**공개** API 들, **인증**이 필요없다.",
            "externalDocs": {
                "description": "External docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
    ]

    debug = True
    TESTING = False

    JWT_PUB_KEY = b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDK5gbX53eEITBJfkg2brNGYnjE5if/F3oRIrray9EZKUhNP2tjUrbQoxhEiT6v7RnhiILeg2bEVFbNhkVdyRn1HdEGlyLweaveR+6uRbtp1G2bbiLba0WY72ncbYQqLWZBEh9kxf13eZa9PZuxdOTRKi+20TWcZrj9UwkFORNEJCwIHJVlQiG0Jr2TZgzpP6WGB7Ayt6XrSbrGoGs1zzk4EGBurl4cxuslCEDn6nUgY3Ia+3xCshgo9oyh9VmN41PPnlzqRvjmwIosaJdeigrw+OLfWUr1O2DfpP/M3jSA5CzRWV0/O7NgX7lS7PTiWpnxYlpvP0UAywWIrs/r6L9FhaP1P0qWOmnmLLLltrxW2LLpCa//qUFWXf6/X63e9bJNF+nvxBFB9ZsG+ki8slRMXrfYLSSSeGHGr8ISTY6p9E7ta2IMvvdhGhAD1NOsrkiiKkiqkOvvdYUKNntRr3RZxPC2l7nHUoteLpNK1CRJAH07afAVGeTy1Z0Ux5XYNPHZBx9QMjemIRrq4g7bLOuLGSNPFk/0aivD6o2T5acnWCqKg0nmRST1/acKZGgxinR6Zy/ZaDVgk/o0GtGGOhpHR5LcLHK5OITPZmfVobVIdpY1SVoy3HnzAw7vIy6ursSisPIV1HdsZLzGCl+DvmMGVudjN+zuWSDqjJAwpm8UIQ== JWT'

    DATA_PATH = Path('./data')
    LOG_PATH = DATA_PATH.joinpath('log')

    CORS_DOMAIN = ['http://127.0.0.1']

    def __init__(self):
        set_directory(self)
        self.app_config = get_app_setting(self)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://beta:beta@192.168.0.99:3306/DEV_ACCOUNT?charset=utf8'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://test:fm$%3t4n5d6j#%$@35.188.65.115:3306/TEST_ACCOUNT?charset=utf8'

    DATA_PATH = Path('./test/data')


class ProductionConfig(Config):
    debug = False
    SQLALCHEMY_DATABASE_URI = 'mysql://account:ac1#c*^o1un&*t@localhost:3306/ACCOUNT?charset=utf8'


env = os.getenv('EXERCIDER_ENV', 'test')


@lru_cache()
def get_settings():
    global env
    config = env

    if config == 'test':
        return TestConfig()
    elif config == 'prod':
        return ProductionConfig()
    else:
        return DevelopmentConfig()


def get_app_setting(cls):
    return {key: getattr(cls, key) for key in dir(cls)
            if key.islower() and not key.startswith('_')}


def set_directory(cls):
    for key in dir(cls):
        if key.endswith('PATH'):
            directory_path = getattr(cls, key)
            if not directory_path.exists():
                directory_path.mkdir(parents=True, exist_ok=True)
