from datetime import date

from app.models.enums import RiskCategory
from app.services.risk_features import FEATURE_NAMES, age_years, extract_features
from app.services.risk_labels import bucket_score, risk_score


def test_age_years_computes_reasonable_value():
    dob = date(1990, 1, 1)
    as_of = date(2020, 1, 1)
    assert 29.9 < age_years(dob, as_of) < 30.1


def test_extract_features_order_matches_feature_names():
    features = extract_features(
        age=40,
        heart_rate=75,
        systolic_bp=115,
        diastolic_bp=75,
        spo2=98,
        temperature=36.8,
        glucose=95,
    )
    assert len(features) == len(FEATURE_NAMES)
    assert features == [40, 75, 115, 75, 98, 36.8, 95]


def test_risk_score_normal_is_zero():
    score = risk_score(
        age=30,
        heart_rate=75,
        systolic_bp=115,
        diastolic_bp=75,
        spo2=98,
        temperature=36.8,
        glucose=95,
    )
    assert score == 0
    assert bucket_score(score) == RiskCategory.LOW


def test_risk_score_elderly_with_abnormal_vitals_is_high():
    score = risk_score(
        age=80,
        heart_rate=145,
        systolic_bp=165,
        diastolic_bp=105,
        spo2=88,
        temperature=39.0,
        glucose=200,
    )
    assert bucket_score(score) == RiskCategory.HIGH


def test_risk_score_mild_deviation_is_moderate():
    score = risk_score(
        age=60,
        heart_rate=105,
        systolic_bp=145,
        diastolic_bp=75,
        spo2=98,
        temperature=36.8,
        glucose=95,
    )
    assert bucket_score(score) == RiskCategory.MODERATE
