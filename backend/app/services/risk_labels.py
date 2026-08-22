from app.models.enums import RiskCategory

# Training-label heuristic for Module 4 (docs/deccission.md ADR-005/ADR-021):
# a simple weighted early-warning-style point score across age + all 5 vitals,
# bucketed into risk categories. Used only to generate supervised training
# labels for scripts/train_risk_model.py — deliberately NOT the same shape as
# app/services/vitals.py's alert-threshold logic (any-one-vital-critical),
# so the classifier learns a genuinely different, non-trivial function from
# the raw feature vector rather than just memorizing the alert rule.


def _points(value: float, low: float, high: float, low2: float, high2: float) -> int:
    if value < low2 or value > high2:
        return 2
    if value < low or value > high:
        return 1
    return 0


def risk_score(
    age: float,
    heart_rate: int,
    systolic_bp: int,
    diastolic_bp: int,
    spo2: int,
    temperature: float,
    glucose: float,
) -> int:
    score = 0
    score += 0 if age < 50 else (1 if age <= 70 else 2)
    score += _points(heart_rate, 60, 100, 50, 120)
    score += _points(systolic_bp, 90, 140, 80, 160)
    score += 0 if diastolic_bp <= 90 else (1 if diastolic_bp <= 100 else 2)
    score += 0 if spo2 >= 95 else (1 if spo2 >= 90 else 2)
    score += _points(temperature, 36.1, 37.5, 35.0, 38.5)
    score += 0 if 70 <= glucose <= 180 else 2
    return score


def bucket_score(score: int) -> RiskCategory:
    if score <= 2:
        return RiskCategory.LOW
    if score <= 5:
        return RiskCategory.MODERATE
    return RiskCategory.HIGH
