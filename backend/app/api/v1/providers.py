from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.patient import Patient
from app.models.provider import Provider
from app.models.user import User
from app.schemas.patient import PatientRead
from app.schemas.provider import AssignPatientRequest, ProviderCreate, ProviderRead

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post("", response_model=ProviderRead, status_code=status.HTTP_201_CREATED)
def create_provider(
    payload: ProviderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> Provider:
    if db.scalar(select(User).where(User.email == payload.email)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists"
        )
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole.DOCTOR,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.flush()

    provider = Provider(
        user_id=user.id,
        full_name=payload.full_name,
        specialty=payload.specialty,
        facility_id=payload.facility_id,
        license_ref=payload.license_ref,
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@router.get("", response_model=list[ProviderRead])
def list_providers(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR, UserRole.EXECUTIVE)),
) -> list[Provider]:
    return list(db.scalars(select(Provider)))


@router.post("/{provider_id}/assign-patient", response_model=PatientRead)
def assign_patient(
    provider_id: int,
    payload: AssignPatientRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> Patient:
    provider = db.get(Provider, provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    patient = db.get(Patient, payload.patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    patient.assigned_provider_id = provider.id
    db.commit()
    db.refresh(patient)
    return patient
