from app.models.enums import AlertSeverity
from app.services.vitals import evaluate_severity

NORMAL = dict(
    heart_rate=75, systolic_bp=115, diastolic_bp=75, spo2=98, temperature=36.8, glucose=95
)


def test_normal_reading_has_no_alert():
    assert evaluate_severity(**NORMAL) is None


def test_moderate_tachycardia_is_medium():
    reading = {**NORMAL, "heart_rate": 110}
    assert evaluate_severity(**reading) == AlertSeverity.MEDIUM


def test_severe_tachycardia_is_high():
    reading = {**NORMAL, "heart_rate": 130}
    assert evaluate_severity(**reading) == AlertSeverity.HIGH


def test_extreme_heart_rate_is_critical():
    reading = {**NORMAL, "heart_rate": 150}
    assert evaluate_severity(**reading) == AlertSeverity.CRITICAL


def test_low_spo2_is_critical():
    reading = {**NORMAL, "spo2": 80}
    assert evaluate_severity(**reading) == AlertSeverity.CRITICAL


def test_mild_low_spo2_is_medium():
    reading = {**NORMAL, "spo2": 93}
    assert evaluate_severity(**reading) == AlertSeverity.MEDIUM


def test_high_fever_is_high():
    reading = {**NORMAL, "temperature": 39.2}
    assert evaluate_severity(**reading) == AlertSeverity.HIGH


def test_high_glucose_is_medium():
    reading = {**NORMAL, "glucose": 200}
    assert evaluate_severity(**reading) == AlertSeverity.MEDIUM
