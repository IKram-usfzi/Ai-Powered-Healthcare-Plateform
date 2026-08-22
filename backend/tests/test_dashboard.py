from datetime import datetime, timezone

from app.models.alert import Alert
from app.models.appointment import Appointment
from app.models.enums import AlertSeverity, RiskCategory, UserRole
from app.models.facility import Facility
from app.models.health_reading import HealthReading
from app.models.prediction import Prediction
from app.models.provider import Provider


def _seed_dashboard_data(db_session, make_user, make_patient):
    facility = Facility(name="Dash Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()

    doc_user = make_user("doc_dash@globalcare-demo.com", "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=doc_user.id,
        full_name="Dr. Dash",
        specialty="Cardiology",
        facility_id=facility.id,
        license_ref="LIC",
    )
    db_session.add(provider)
    db_session.commit()

    patient = make_patient(full_name="Dash Patient")
    patient.assigned_provider_id = provider.id
    db_session.commit()

    now = datetime.now(timezone.utc)
    db_session.add(Appointment(patient_id=patient.id, provider_id=provider.id, scheduled_at=now))
    reading = HealthReading(
        patient_id=patient.id,
        heart_rate=75,
        systolic_bp=115,
        diastolic_bp=75,
        spo2=98,
        temperature=36.8,
        glucose=95,
        recorded_at=now,
    )
    db_session.add(reading)
    db_session.commit()
    db_session.add(
        Alert(patient_id=patient.id, reading_id=reading.id, severity=AlertSeverity.CRITICAL)
    )
    db_session.add(
        Prediction(
            patient_id=patient.id,
            risk_category=RiskCategory.HIGH,
            confidence_score=0.9,
            model_version="test-v1",
            recommendation="Urgent review",
        )
    )
    db_session.commit()

    return doc_user, provider, patient


def test_overview_requires_admin_or_executive(client, make_user, auth_header):
    doc = make_user("doc_dash_denied@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.get("/api/v1/dashboard/overview", headers=auth_header(doc))
    assert response.status_code == 403


def test_overview_reflects_real_data(client, make_user, make_patient, auth_header, db_session):
    admin = make_user("admin_dash1@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    _, _, patient = _seed_dashboard_data(db_session, make_user, make_patient)

    response = client.get("/api/v1/dashboard/overview", headers=auth_header(admin))
    assert response.status_code == 200
    body = response.json()
    assert body["total_patients"] == 1
    assert body["appointments_today"] == 1
    assert body["active_monitoring_patients"] == 1
    assert body["high_risk_patients"] == 1
    assert body["open_alerts"] == 1
    assert body["critical_alerts"] == 1
    assert len(body["top_risk_patients"]) == 1
    assert body["appointments_today_by_status"] == {"scheduled": 1}
    assert body["top_risk_patients"][0]["patient_id"] == patient.id


def test_trends_requires_executive_specifically(client, make_user, auth_header):
    admin = make_user("admin_dash2@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    response = client.get("/api/v1/dashboard/trends", headers=auth_header(admin))
    assert response.status_code == 403


def test_trends_returns_7_days_including_todays_activity(
    client, make_user, make_patient, auth_header, db_session
):
    executive = make_user("exec_dash1@globalcare-demo.com", "pw", UserRole.EXECUTIVE)
    _seed_dashboard_data(db_session, make_user, make_patient)

    response = client.get("/api/v1/dashboard/trends", headers=auth_header(executive))
    assert response.status_code == 200
    days = response.json()["days"]
    assert len(days) == 7
    today = days[-1]
    assert today["readings_count"] == 1
    assert today["alerts_count"] == 1


def test_provider_activity_reflects_real_data(
    client, make_user, make_patient, auth_header, db_session
):
    executive = make_user("exec_dash2@globalcare-demo.com", "pw", UserRole.EXECUTIVE)
    _, provider, _ = _seed_dashboard_data(db_session, make_user, make_patient)

    response = client.get("/api/v1/dashboard/provider-activity", headers=auth_header(executive))
    assert response.status_code == 200
    rows = [r for r in response.json() if r["provider_id"] == provider.id]
    assert len(rows) == 1
    assert rows[0]["assigned_patients"] == 1
    assert rows[0]["appointments_today"] == 1


def test_executive_report_requires_executive(client, make_user, auth_header):
    admin = make_user("admin_dash3@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    response = client.get("/api/v1/reports/executive", headers=auth_header(admin))
    assert response.status_code == 403


def test_executive_report_combines_all_sections(
    client, make_user, make_patient, auth_header, db_session
):
    executive = make_user("exec_dash3@globalcare-demo.com", "pw", UserRole.EXECUTIVE)
    _seed_dashboard_data(db_session, make_user, make_patient)

    response = client.get("/api/v1/reports/executive", headers=auth_header(executive))
    assert response.status_code == 200
    body = response.json()
    assert body["overview"]["total_patients"] == 1
    assert len(body["trends"]["days"]) == 7
    assert len(body["provider_activity"]) == 1
    assert body["generated_at"]
