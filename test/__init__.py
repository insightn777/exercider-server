import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from configs import get_settings
from main import create

setting = get_settings()
database = create_engine(setting.SQLALCHEMY_DATABASE_URI, encoding='utf-8')


@pytest.fixture()
def app():
    app = create(setting)
    yield app


@pytest.fixture
def client(app):
    try:
        assert setting.TESTING is True
    except AssertionError:
        database.close()
        pytest.exit('test config value is wrong, stop test')

    return TestClient(app)
