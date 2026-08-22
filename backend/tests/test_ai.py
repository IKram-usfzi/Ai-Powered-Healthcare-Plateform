from datetime import datetime, timezone

from app.models.enums import UserRole
from app.models.facility import Facility
from app.models.health_reading import HealthReading
from app.models.provider import Provider


def _make_assigned_patient_with_reading(db_session, make_user, make_patient):
    facility = Facility(name="Test Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()

    doc_user = make_user("doc_ai@globalcare-demo.com", "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=doc_user.id,
        full_name="Dr. AI",
        specialty="General",
        facility_id=facility.id,
        license_ref="LIC",
    )
    db_session.add(provider)
    db_session.commit()

    patient_user = make_user("pat_ai@globalcare-demo.com", "pw", UserRole.PATIENT)
    patient = make_patient(user=patient_user)
    patient.assigned_provider_id = provider.id
    db_session.commit()

    reading = HealthReading(
        patient_id=patient.id,
        heart_rate=75,
        systolic_bp=115,
        diastolic_bp=75,
        spo2=98,
        temperature=36.8,
        glucose=95,
        recorded_at=datetime.now(timezone.utc),
    )
    db_session.add(reading)
    db_session.commit()

    return doc_user, patient_user, patient


def test_non_doctor_cannot_run_risk_assessment(client, make_user, make_patient, auth_header):
    admin = make_user("admin_ai1@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient = make_patient()
    response = client.post(
        "/api/v1/ai/risk-assessment", json={"patient_id": patient.id}, headers=auth_header(admin)
    )
    assert response.status_code == 403


def test_doctor_not_assigned_denied(client, make_user, make_patient, auth_header, db_session):
    _, _, patient = _make_assigned_patient_with_reading(db_session, make_user, make_patient)
    other_doc = make_user("otherdoc_ai@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.post(
        "/api/v1/ai/risk-assessment",
        json={"patient_id": patient.id},
        headers=auth_header(other_doc),
    )
    assert response.status_code == 403


def test_unknown_patient_404(client, make_user, auth_header):
    doc = make_user("doc_ai_404@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.post(
        "/api/v1/ai/risk-assessment", json={"patient_id": 999999}, headers=auth_header(doc)
    )
    assert response.status_code == 404


def test_patient_with_no_readings_gets_400(
    client, make_user, make_patient, auth_header, db_session
):
    facility = Facility(name="F2", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()
    doc_user = make_user("doc_ai_noread@globalcare-demo.com", "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=doc_user.id,
        full_name="Dr. NoRead",
        specialty="General",
        facility_id=facility.id,
        license_ref="LIC2",
    )
    db_session.add(provider)
    db_session.commit()
    patient = make_patient()
    patient.assigned_provider_id = provider.id
    db_session.commit()

    response = client.post(
        "/api/v1/ai/risk-assessment", json={"patient_id": patient.id}, headers=auth_header(doc_user)
    )
    assert response.status_code == 400


def test_risk_assessment_produces_and_stores_prediction(
    client, make_user, make_patient, auth_header, db_session
):
    doc_user, patient_user, patient = _make_assigned_patient_with_reading(
        db_session, make_user, make_patient
    )

    response = client.post(
        "/api/v1/ai/risk-assessment", json={"patient_id": patient.id}, headers=auth_header(doc_user)
    )
    assert response.status_code == 201
    body = response.json()
    assert body["patient_id"] == patient.id
    assert body["risk_category"] in ("low", "moderate", "high")
    assert 0.0 <= body["confidence_score"] <= 1.0
    assert body["model_version"]
    assert "clinical judgement" in body["recommendation"]

    history = client.get(f"/api/v1/ai/predictions/{patient.id}", headers=auth_header(doc_user))
    assert history.status_code == 200
    assert len(history.json()) == 1

    self_history = client.get(
        f"/api/v1/ai/predictions/{patient.id}", headers=auth_header(patient_user)
    )
    assert self_history.status_code == 200

    other_patient_user = make_user("otherpat_ai@globalcare-demo.com", "pw", UserRole.PATIENT)
    make_patient(user=other_patient_user)
    denied = client.get(
        f"/api/v1/ai/predictions/{patient.id}", headers=auth_header(other_patient_user)
    )
    assert denied.status_code == 403


def test_model_metadata_requires_admin(client, make_user, auth_header):
    doc = make_user("doc_ai_meta@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.get("/api/v1/ai/model/metadata", headers=auth_header(doc))
    assert response.status_code == 403


def test_model_metadata_returns_training_summary(client, make_user, auth_header):
    admin = make_user("admin_ai_meta@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    response = client.get("/api/v1/ai/model/metadata", headers=auth_header(admin))
    assert response.status_code == 200
    body = response.json()
    assert body["algorithm"] == "RandomForestClassifier"
    assert body["model_version"]
    assert 0.0 <= body["accuracy"] <= 1.0
