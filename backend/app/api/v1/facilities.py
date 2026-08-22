from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.enums import UserRole
from app.models.facility import Facility
from app.models.user import User
from app.schemas.facility import FacilityCreate, FacilityRead

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.post("", response_model=FacilityRead, status_code=status.HTTP_201_CREATED)
def create_facility(
    payload: FacilityCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> Facility:
    facility = Facility(**payload.model_dump())
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility
