from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.appointment import Appointment
from app.models.consultation import Consultation
from app.models.enums import AppointmentStatus, UserRole
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentStatusUpdate
from app.schemas.consultation import ConsultationCreate, ConsultationRead

router = APIRouter(tags=["appointments"])


@router.post("/appointments", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.PATIENT, UserRole.ADMINISTRATOR)),
) -> Appointment:
    if current_user.role == UserRole.PATIENT:
        if current_user.patient is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No patient record linked to this user",
            )
        patient_id = current_user.patient.id
    else:
        if payload.patient_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="patient_id is required when an administrator books an appointment",
            )
        patient_id = payload.patient_id

    appointment = Appointment(
        patient_id=patient_id, provider_id=payload.provider_id, scheduled_at=payload.scheduled_at
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/appointments", response_model=list[AppointmentRead])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.DOCTOR, UserRole.ADMINISTRATOR, UserRole.PATIENT)
    ),
) -> list[Appointment]:
    stmt = select(Appointment)
    if current_user.role == UserRole.DOCTOR:
        if current_user.provider is None:
            return []
        stmt = stmt.where(Appointment.provider_id == current_user.provider.id)
    elif current_user.role == UserRole.PATIENT:
        if current_user.patient is None:
            return []
        stmt = stmt.where(Appointment.patient_id == current_user.patient.id)
    return list(db.scalars(stmt))


def _get_appointment_or_404(db: Session, appointment_id: int) -> Appointment:
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


@router.patch("/appointments/{appointment_id}/status", response_model=AppointmentRead)
def update_appointment_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.DOCTOR, UserRole.ADMINISTRATOR)),
) -> Appointment:
    appointment = _get_appointment_or_404(db, appointment_id)
    if current_user.role == UserRole.DOCTOR:
        if current_user.provider is None or appointment.provider_id != current_user.provider.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this appointment",
            )
    appointment.status = payload.status
    db.commit()
    db.refresh(appointment)
    return appointment


@router.post("/consultations", response_model=ConsultationRead, status_code=status.HTTP_201_CREATED)
def create_consultation(
    payload: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.DOCTOR)),
) -> Consultation:
    appointment = _get_appointment_or_404(db, payload.appointment_id)
    if current_user.provider is None or appointment.provider_id != current_user.provider.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to record a consultation for this appointment",
        )
    if appointment.consultation is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A consultation has already been recorded for this appointment",
        )

    consultation = Consultation(
        appointment_id=payload.appointment_id,
        summary=payload.summary,
        recommendations=payload.recommendations,
    )
    appointment.status = AppointmentStatus.COMPLETED
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return consultation


@router.get("/consultations/{patient_id}", response_model=list[ConsultationRead])
def get_consultation_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.DOCTOR, UserRole.ADMINISTRATOR, UserRole.PATIENT)
    ),
) -> list[Consultation]:
    if current_user.role == UserRole.PATIENT:
        if current_user.patient is None or current_user.patient.id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this consultation history",
            )

    stmt = (
        select(Consultation)
        .join(Appointment, Consultation.appointment_id == Appointment.id)
        .where(Appointment.patient_id == patient_id)
    )
    if current_user.role == UserRole.DOCTOR:
        # Security.md §3: a doctor may read/write only their assigned patients' records
        if current_user.provider is None:
            return []
        stmt = stmt.where(Appointment.provider_id == current_user.provider.id)
    return list(db.scalars(stmt))
