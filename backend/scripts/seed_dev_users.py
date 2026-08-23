"""Create one login per role (Administrator, Executive, Doctor, Patient) for
local/demo login.

The documented API (docs/api-spec.md) has no "create administrator" endpoint —
administrators and executives are assumed to be provisioned out-of-band. This
script is that out-of-band provisioning step for a dev/demo environment. The
Doctor and Patient accounts are linked domain records (Provider/Patient, with
the patient assigned to the doctor) so every role-scoped feature — recording
a consultation, acknowledging an alert, running an AI risk assessment,
booking an appointment — is actually demoable, not just the two auth-only
roles.

DEV/DEMO CREDENTIALS ONLY — never use this in a real deployment.

Usage:
    python scripts/seed_dev_users.py
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.base import Base, SessionLocal, engine  # noqa: E402
from app.models.enums import UserRole  # noqa: E402
from app.models.facility import Facility  # noqa: E402
from app.models.patient import Patient  # noqa: E402
from app.models.provider import Provider  # noqa: E402
from app.models.user import User  # noqa: E402

DEV_PASSWORD = "ChangeMe123!"

DEV_USERS = [
    ("admin@globalcare-demo.com", UserRole.ADMINISTRATOR),
    ("executive@globalcare-demo.com", UserRole.EXECUTIVE),
]

DEMO_DOCTOR_EMAIL = "doctor@globalcare-demo.com"
DEMO_PATIENT_EMAIL = "patient@globalcare-demo.com"


def _seed_auth_only_users(session) -> None:
    for email, role in DEV_USERS:
        if session.scalar(select(User).where(User.email == email)) is not None:
            print(f"Already exists: {email}")
            continue
        session.add(User(email=email, password_hash=hash_password(DEV_PASSWORD), role=role))
        print(f"Created: {email} ({role.value}) / password: {DEV_PASSWORD}")


def _seed_demo_doctor_and_patient(session) -> None:
    """A doctor with an assigned patient - runs before seed_synthea.py in the
    documented setup order (installation-guide.md), so it can't assume any
    facility/provider/patient rows exist yet."""
    if session.scalar(select(User).where(User.email == DEMO_DOCTOR_EMAIL)) is not None:
        print(f"Already exists: {DEMO_DOCTOR_EMAIL}")
        return

    facility = session.scalar(select(Facility).limit(1))
    if facility is None:
        facility = Facility(name="GlobalCare Demo Clinic", type="Clinic", location="Demo City")
        session.add(facility)
        session.flush()

    doctor_user = User(
        email=DEMO_DOCTOR_EMAIL, password_hash=hash_password(DEV_PASSWORD), role=UserRole.DOCTOR
    )
    session.add(doctor_user)
    session.flush()
    provider = Provider(
        user_id=doctor_user.id,
        full_name="Dr. Demo Doctor",
        specialty="General Practice",
        facility_id=facility.id,
        license_ref="DEMO-0001",
    )
    session.add(provider)
    session.flush()

    patient_user = User(
        email=DEMO_PATIENT_EMAIL, password_hash=hash_password(DEV_PASSWORD), role=UserRole.PATIENT
    )
    session.add(patient_user)
    session.flush()
    session.add(
        Patient(
            user_id=patient_user.id,
            full_name="Demo Patient",
            date_of_birth=date(1985, 6, 15),
            gender="Female",
            contact_info="555-0100",
            assigned_provider_id=provider.id,
        )
    )

    print(f"Created: {DEMO_DOCTOR_EMAIL} (doctor) / password: {DEV_PASSWORD}")
    print(
        f"Created: {DEMO_PATIENT_EMAIL} (patient, assigned to Dr. Demo Doctor) / "
        f"password: {DEV_PASSWORD}"
    )


def seed() -> None:
    Base.metadata.create_all(engine)
    session = SessionLocal()

    _seed_auth_only_users(session)
    _seed_demo_doctor_and_patient(session)

    session.commit()
    session.close()


if __name__ == "__main__":
    seed()
