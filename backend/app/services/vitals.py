from app.models.enums import AlertSeverity

# Threshold-based abnormal-reading detection (docs/flow.md §3, docs/PRD.md §6
# Module 3). Reasonable general adult ranges for a decision-support POC — not
# a certified clinical device, never a diagnosis (docs/PRD.md §7).


def evaluate_severity(
    heart_rate: int,
    systolic_bp: int,
    diastolic_bp: int,
    spo2: int,
    temperature: float,
    glucose: float,
) -> AlertSeverity | None:
    if (
        spo2 < 85
        or heart_rate > 140
        or heart_rate < 40
        or systolic_bp > 180
        or systolic_bp < 80
        or temperature >= 40
        or temperature <= 34
    ):
        return AlertSeverity.CRITICAL

    if (
        spo2 < 90
        or heart_rate > 120
        or heart_rate < 50
        or systolic_bp > 160
        or diastolic_bp > 120
        or temperature >= 39
    ):
        return AlertSeverity.HIGH

    if (
        spo2 < 95
        or heart_rate > 100
        or heart_rate < 60
        or systolic_bp > 140
        or systolic_bp < 90
        or diastolic_bp > 90
        or diastolic_bp < 60
        or temperature >= 38
        or temperature <= 35.5
        or glucose > 180
        or glucose < 70
    ):
        return AlertSeverity.MEDIUM

    return None
