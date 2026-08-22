from app.models.enums import UserRole
from app.models.facility import Facility
from app.models.provider import Provider

NORMAL_READING = {
    "heart_rate": 75,
    "systolic_bp": 115,
    "diastolic_bp": 75,
    "spo2": 98,
    "temperature": 36.8,
    "glucose": 95,
}
ABNORMAL_READING = {**NORMAL_READING, "heart_rate": 150, "spo2": 80}


def _make_assigned_pair(db_session, make_user, make_patient):
    facility = Facility(name="Test Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()

    doc_user = make_user("doc_mon@globalcare-demo.com", "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=doc_user.id,
        full_name="Dr. Monitor",
        specialty="General",
        facility_id=facility.id,
        license_ref="LIC",
    )
    db_session.add(provider)
    db_session.commit()

    patient_user = make_user("pat_mon@globalcare-demo.com", "pw", UserRole.PATIENT)
    patient = make_patient(user=patient_user)
    patient.assigned_provider_id = provider.id
    db_session.commit()

    return doc_user, provider, patient_user, patient


def test_patient_can_ingest_own_reading(client, make_user, make_patient, auth_header):
    patient_user = make_user("selfmon@globalcare-demo.com", "pw", UserRole.PATIENT)
    make_patient(user=patient_user)

    response = client.post(
        "/api/v1/monitoring/readings", json=NORMAL_READING, headers=auth_header(patient_user)
    )
    assert response.status_code == 201
    assert response.json()["heart_rate"] == 75


def test_non_patient_cannot_ingest_reading(client, make_user, auth_header):
    admin = make_user("admin_mon1@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    response = client.post(
        "/api/v1/monitoring/readings", json=NORMAL_READING, headers=auth_header(admin)
    )
    assert response.status_code == 403


def test_patient_without_linked_record_gets_400(client, make_user, auth_header):
    patient_user = make_user("nopat@globalcare-demo.com", "pw", UserRole.PATIENT)
    response = client.post(
        "/api/v1/monitoring/readings", json=NORMAL_READING, headers=auth_header(patient_user)
    )
    assert response.status_code == 400


def test_normal_reading_produces_no_alert(client, make_user, make_patient, auth_header, db_session):
    doc_user, _, patient_user, _ = _make_assigned_pair(db_session, make_user, make_patient)
    client.post(
        "/api/v1/monitoring/readings", json=NORMAL_READING, headers=auth_header(patient_user)
    )

    alerts = client.get("/api/v1/monitoring/alerts", headers=auth_header(doc_user))
    assert alerts.json() == []


def test_abnormal_reading_produces_exactly_one_alert_deduped(
    client, make_user, make_patient, auth_header, db_session
):
    """Phase 4 exit criteria (impmemnentaion-plan.md): a simulated abnormal
    reading produces exactly one alert, verified via Redis de-dup."""
    doc_user, provider, patient_user, patient = _make_assigned_pair(
        db_session, make_user, make_patient
    )

    # three abnormal readings in a row for the same patient
    for _ in range(3):
        resp = client.post(
            "/api/v1/monitoring/readings", json=ABNORMAL_READING, headers=auth_header(patient_user)
        )
        assert resp.status_code == 201

    alerts = client.get("/api/v1/monitoring/alerts", headers=auth_header(doc_user))
    assert alerts.status_code == 200
    assert len(alerts.json()) == 1
    assert alerts.json()[0]["severity"] == "critical"
    assert alerts.json()[0]["patient_id"] == patient.id


def test_reading_history_access_scoping(client, make_user, make_patient, auth_header, db_session):
    doc_user, provider, patient_user, patient = _make_assigned_pair(
        db_session, make_user, make_patient
    )
    client.post(
        "/api/v1/monitoring/readings", json=NORMAL_READING, headers=auth_header(patient_user)
    )

    own = client.get(f"/api/v1/monitoring/readings/{patient.id}", headers=auth_header(patient_user))
    assert own.status_code == 200
    assert len(own.json()) == 1

    doctor_view = client.get(
        f"/api/v1/monitoring/readings/{patient.id}", headers=auth_header(doc_user)
    )
    assert doctor_view.status_code == 200

    other_doc = make_user("otherdoc_mon@globalcare-demo.com", "pw", UserRole.DOCTOR)
    denied = client.get(f"/api/v1/monitoring/readings/{patient.id}", headers=auth_header(other_doc))
    assert denied.status_code == 403

    other_patient_user = make_user("otherpat_mon@globalcare-demo.com", "pw", UserRole.PATIENT)
    make_patient(user=other_patient_user)
    denied_patient = client.get(
        f"/api/v1/monitoring/readings/{patient.id}", headers=auth_header(other_patient_user)
    )
    assert denied_patient.status_code == 403


def test_acknowledge_alert(client, make_user, make_patient, auth_header, db_session):
    doc_user, provider, patient_user, patient = _make_assigned_pair(
        db_session, make_user, make_patient
    )
    client.post(
        "/api/v1/monitoring/readings", json=ABNORMAL_READING, headers=auth_header(patient_user)
    )
    alert_id = client.get("/api/v1/monitoring/alerts", headers=auth_header(doc_user)).json()[0][
        "id"
    ]

    other_doc = make_user("otherdoc_mon2@globalcare-demo.com", "pw", UserRole.DOCTOR)
    denied = client.patch(
        f"/api/v1/monitoring/alerts/{alert_id}/acknowledge", headers=auth_header(other_doc)
    )
    assert denied.status_code == 403

    response = client.patch(
        f"/api/v1/monitoring/alerts/{alert_id}/acknowledge", headers=auth_header(doc_user)
    )
    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"

    # acknowledged alerts still show (only resolved is excluded from the "active" list)
    still_listed = client.get("/api/v1/monitoring/alerts", headers=auth_header(doc_user))
    assert len(still_listed.json()) == 1


def test_acknowledge_unknown_alert_404(client, make_user, auth_header):
    doc = make_user("doc_mon_404@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.patch(
        "/api/v1/monitoring/alerts/999999/acknowledge", headers=auth_header(doc)
    )
    assert response.status_code == 404


def test_list_alerts_requires_doctor_or_admin(client, make_user, auth_header):
    patient_user = make_user("patmon_denied@globalcare-demo.com", "pw", UserRole.PATIENT)
    response = client.get("/api/v1/monitoring/alerts", headers=auth_header(patient_user))
    assert response.status_code == 403
