import enum


class UserRole(str, enum.Enum):
    """docs/backend-schema.md §2 (users); docs/api-spec.md §1."""

    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMINISTRATOR = "administrator"
    EXECUTIVE = "executive"


class AppointmentStatus(str, enum.Enum):
    """docs/backend-schema.md §2 (appointments)."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AlertSeverity(str, enum.Enum):
    """docs/flow.md §3 (abnormal-reading detection)."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    """docs/backend-schema.md §2 (alerts)."""

    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class RiskCategory(str, enum.Enum):
    """docs/flow.md §4 (AI prediction workflow)."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
