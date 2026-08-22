from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401  (registers all 9 tables on Base.metadata)
from app.api.deps import get_db
from app.core.redis_client import get_redis
from app.core.security import create_token, hash_password
from app.db.base import Base
from app.main import app
from app.models.enums import UserRole
from app.models.patient import Patient
from app.models.user import User


class FakeRedis:
    """In-memory stand-in for redis.Redis — enough for the dedup logic
    (app/api/v1/monitoring.py) to be tested without a real Redis server."""

    def __init__(self):
        self._store: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._store.get(key)

    def set(self, key: str, value: str, ex: int | None = None) -> bool:
        self._store[key] = value
        return True


@pytest.fixture()
def db_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_local()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def fake_redis():
    return FakeRedis()


@pytest.fixture()
def client(db_session, fake_redis):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = lambda: fake_redis
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def make_user(db_session):
    def _make(email: str, password: str, role: UserRole) -> User:
        user = User(email=email, password_hash=hash_password(password), role=role)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _make


@pytest.fixture()
def make_patient(db_session):
    def _make(full_name: str = "Test Patient", user: User | None = None) -> Patient:
        patient = Patient(
            full_name=full_name,
            date_of_birth=date(1990, 1, 1),
            gender="Male",
            contact_info="123 Test St",
            user_id=user.id if user else None,
        )
        db_session.add(patient)
        db_session.commit()
        db_session.refresh(patient)
        return patient

    return _make


@pytest.fixture()
def auth_header():
    def _header(user: User) -> dict:
        token = create_token(str(user.id), user.role.value, "access")
        return {"Authorization": f"Bearer {token}"}

    return _header
