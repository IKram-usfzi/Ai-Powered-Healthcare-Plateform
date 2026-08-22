from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.opa_client import OPAClient, get_opa_client
from app.core.security import decode_token
from app.db.base import get_db
from app.models.enums import UserRole
from app.models.user import User

# tokenUrl is documentation-only here; login is a JSON POST, not an OAuth2 form
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise unauthorized
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise unauthorized
    user = db.get(User, int(payload["sub"]))
    if user is None:
        raise unauthorized
    return user


def require_roles(*roles: UserRole):
    """docs/deccission.md ADR-006/ADR-024: the allow/deny decision is delegated
    to OPA's allow_role Rego rule (infra/opa/policies/authz.rego) rather than a
    Python `in` check — this only builds the input document and enforces OPA's
    decision. Row-level checks (e.g. "doctor's own assigned patients") stay in
    the API layer per Security.md §9, not in OPA — see ADR-024 for why."""
    allowed = [role.value for role in roles]

    def checker(
        current_user: User = Depends(get_current_user),
        opa: OPAClient = Depends(get_opa_client),
    ) -> User:
        if not opa.allow_role(current_user.role.value, allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return checker
