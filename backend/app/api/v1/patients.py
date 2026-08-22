from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models.enums import UserRole
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> Patient:
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("", response_model=list[PatientRead])
def list_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMINISTRATOR, UserRole.DOCTOR)),
) -> list[Patient]:
    stmt = select(Patient)
    if current_user.role == UserRole.DOCTOR:
        # Security.md §3: a doctor may read/write only their assigned patients' records
        if current_user.provider is None:
            return []
        stmt = stmt.where(Patient.assigned_provider_id == current_user.provider.id)
    return list(db.scalars(stmt))


def _get_patient_or_404(db: Session, patient_id: int) -> Patient:
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


def _authorize_patient_access(patient: Patient, current_user: User) -> None:
    if current_user.role == UserRole.ADMINISTRATOR:
        return
    if current_user.role == UserRole.DOCTOR:
        if current_user.provider and patient.assigned_provider_id == current_user.provider.id:
            return
    elif current_user.role == UserRole.PATIENT:
        if current_user.patient and patient.id == current_user.patient.id:
            return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this patient's record",
    )


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Patient:
    patient = _get_patient_or_404(db, patient_id)
    _authorize_patient_access(patient, current_user)
    return patient


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> Patient:
    patient = _get_patient_or_404(db, patient_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient
