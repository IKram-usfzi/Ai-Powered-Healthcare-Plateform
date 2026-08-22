from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401  (registers all 9 tables on Base.metadata)
from app.api.deps import get_db
from app.core.security import create_token, hash_password
from app.db.base import Base
from app.main import app
from app.models.enums import UserRole
from app.models.patient import Patient
from app.models.user import User


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
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
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
