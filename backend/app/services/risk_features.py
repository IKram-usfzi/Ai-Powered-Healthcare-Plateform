from datetime import date

FEATURE_NAMES = [
    "age_years",
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "spo2",
    "temperature",
    "glucose",
]


def age_years(date_of_birth: date, as_of: date) -> float:
    return (as_of - date_of_birth).days / 365.25


def extract_features(
    age: float,
    heart_rate: int,
    systolic_bp: int,
    diastolic_bp: int,
    spo2: int,
    temperature: float,
    glucose: float,
) -> list[float]:
    """Fixed-order feature vector shared by scripts/train_risk_model.py (training)
    and app/api/v1/ai.py (inference) — must stay identical on both sides to avoid
    train/serve skew."""
    return [age, heart_rate, systolic_bp, diastolic_bp, spo2, temperature, glucose]
