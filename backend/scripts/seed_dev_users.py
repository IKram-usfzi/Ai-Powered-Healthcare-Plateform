"""Create one Administrator and one Executive user for local/demo login.

The documented API (docs/api-spec.md) has no "create administrator" endpoint —
administrators and executives are assumed to be provisioned out-of-band. This
script is that out-of-band provisioning step for a dev/demo environment.

DEV/DEMO CREDENTIALS ONLY — never use this in a real deployment.

Usage:
    python scripts/seed_dev_users.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.base import Base, SessionLocal, engine  # noqa: E402
from app.models.enums import UserRole  # noqa: E402
from app.models.user import User  # noqa: E402

DEV_PASSWORD = "ChangeMe123!"

DEV_USERS = [
    ("admin@globalcare-demo.com", UserRole.ADMINISTRATOR),
    ("executive@globalcare-demo.com", UserRole.EXECUTIVE),
]


def seed() -> None:
    Base.metadata.create_all(engine)
    session = SessionLocal()

    for email, role in DEV_USERS:
        if session.scalar(select(User).where(User.email == email)) is not None:
            print(f"Already exists: {email}")
            continue
        session.add(User(email=email, password_hash=hash_password(DEV_PASSWORD), role=role))
        print(f"Created: {email} ({role.value}) / password: {DEV_PASSWORD}")

    session.commit()
    session.close()


if __name__ == "__main__":
    seed()
