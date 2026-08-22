from datetime import datetime, timedelta, timezone

from app.models.enums import UserRole
from app.models.facility import Facility
from app.models.provider import Provider


def _make_provider(db_session, make_user, email="doc@globalcare-demo.com"):
    facility = Facility(name="Test Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()

    provider_user = make_user(email, "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=provider_user.id,
        full_name="Dr. Test",
        specialty="General",
        facility_id=facility.id,
        license_ref="LIC",
    )
    db_session.add(provider)
    db_session.commit()
    return provider_user, provider


FUTURE = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()


def test_patient_can_book_appointment_for_self(
    client, make_user, make_patient, auth_header, db_session
):
    _, provider = _make_provider(db_session, make_user)
    patient_user = make_user("pat1@globalcare-demo.com", "pw", UserRole.PATIENT)
    patient = make_patient(user=patient_user)

    response = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE},
        headers=auth_header(patient_user),
    )
    assert response.status_code == 201
    assert response.json()["patient_id"] == patient.id
    assert response.json()["status"] == "scheduled"


def test_admin_must_supply_patient_id(client, make_user, auth_header, db_session):
    _, provider = _make_provider(db_session, make_user)
    admin = make_user("admin_appt1@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)

    response = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE},
        headers=auth_header(admin),
    )
    assert response.status_code == 400


def test_doctor_cannot_book_appointment(client, make_user, db_session, auth_header):
    _, provider = _make_provider(db_session, make_user, "doc2@globalcare-demo.com")
    other_doc = make_user("doc3@globalcare-demo.com", "pw", UserRole.DOCTOR)

    response = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE},
        headers=auth_header(other_doc),
    )
    assert response.status_code == 403


def test_appointment_lists_are_scoped_per_role(
    client, make_user, make_patient, auth_header, db_session
):
    _, provider = _make_provider(db_session, make_user, "doc4@globalcare-demo.com")
    admin = make_user("admin_appt2@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient_user = make_user("pat2@globalcare-demo.com", "pw", UserRole.PATIENT)
    patient = make_patient(user=patient_user)
    other_patient = make_patient(full_name="Other Patient")

    client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": patient.id},
        headers=auth_header(admin),
    )
    client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": other_patient.id},
        headers=auth_header(admin),
    )

    admin_view = client.get("/api/v1/appointments", headers=auth_header(admin))
    assert len(admin_view.json()) == 2

    patient_view = client.get("/api/v1/appointments", headers=auth_header(patient_user))
    assert len(patient_view.json()) == 1
    assert patient_view.json()[0]["patient_id"] == patient.id


def test_update_appointment_status_role_scoping(
    client, make_user, make_patient, auth_header, db_session
):
    doc_user, provider = _make_provider(db_session, make_user, "doc5@globalcare-demo.com")
    other_doc = make_user("doc6@globalcare-demo.com", "pw", UserRole.DOCTOR)
    admin = make_user("admin_appt3@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient = make_patient()

    appt = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": patient.id},
        headers=auth_header(admin),
    ).json()

    denied = client.patch(
        f"/api/v1/appointments/{appt['id']}/status",
        json={"status": "in_progress"},
        headers=auth_header(other_doc),
    )
    assert denied.status_code == 403

    allowed = client.patch(
        f"/api/v1/appointments/{appt['id']}/status",
        json={"status": "in_progress"},
        headers=auth_header(doc_user),
    )
    assert allowed.status_code == 200
    assert allowed.json()["status"] == "in_progress"


def test_update_unknown_appointment_404(client, make_user, auth_header):
    admin = make_user("admin_appt4@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    response = client.patch(
        "/api/v1/appointments/999999/status",
        json={"status": "cancelled"},
        headers=auth_header(admin),
    )
    assert response.status_code == 404


def test_consultation_lifecycle(client, make_user, make_patient, auth_header, db_session):
    doc_user, provider = _make_provider(db_session, make_user, "doc7@globalcare-demo.com")
    other_doc = make_user("doc8@globalcare-demo.com", "pw", UserRole.DOCTOR)
    admin = make_user("admin_appt5@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient = make_patient()

    appt = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": patient.id},
        headers=auth_header(admin),
    ).json()

    # wrong doctor can't record a consultation for someone else's appointment
    denied = client.post(
        "/api/v1/consultations",
        json={"appointment_id": appt["id"], "summary": "s", "recommendations": "r"},
        headers=auth_header(other_doc),
    )
    assert denied.status_code == 403

    created = client.post(
        "/api/v1/consultations",
        json={
            "appointment_id": appt["id"],
            "summary": "Routine checkup",
            "recommendations": "Rest",
        },
        headers=auth_header(doc_user),
    )
    assert created.status_code == 201

    # appointment auto-completed
    updated_appt = client.get("/api/v1/appointments", headers=auth_header(admin)).json()
    assert updated_appt[0]["status"] == "completed"

    # duplicate consultation rejected
    duplicate = client.post(
        "/api/v1/consultations",
        json={"appointment_id": appt["id"], "summary": "again", "recommendations": "again"},
        headers=auth_header(doc_user),
    )
    assert duplicate.status_code == 409

    # patient role can't record consultations at all
    patient_user = make_user("pat3@globalcare-demo.com", "pw", UserRole.PATIENT)
    role_denied = client.post(
        "/api/v1/consultations",
        json={"appointment_id": appt["id"], "summary": "x", "recommendations": "y"},
        headers=auth_header(patient_user),
    )
    assert role_denied.status_code == 403


def test_consultation_history_access(client, make_user, make_patient, auth_header, db_session):
    doc_user, provider = _make_provider(db_session, make_user, "doc9@globalcare-demo.com")
    admin = make_user("admin_appt6@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient_user = make_user("pat4@globalcare-demo.com", "pw", UserRole.PATIENT)
    patient = make_patient(user=patient_user)
    other_patient_user = make_user("pat5@globalcare-demo.com", "pw", UserRole.PATIENT)
    make_patient(user=other_patient_user)

    appt = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": patient.id},
        headers=auth_header(admin),
    ).json()
    client.post(
        "/api/v1/consultations",
        json={"appointment_id": appt["id"], "summary": "s", "recommendations": "r"},
        headers=auth_header(doc_user),
    )

    own = client.get(f"/api/v1/consultations/{patient.id}", headers=auth_header(patient_user))
    assert own.status_code == 200
    assert len(own.json()) == 1

    other = client.get(
        f"/api/v1/consultations/{patient.id}", headers=auth_header(other_patient_user)
    )
    assert other.status_code == 403

    admin_view = client.get(f"/api/v1/consultations/{patient.id}", headers=auth_header(admin))
    assert admin_view.status_code == 200
    assert len(admin_view.json()) == 1


def test_provider_schedule_access(client, make_user, make_patient, auth_header, db_session):
    doc_user, provider = _make_provider(db_session, make_user, "doc10@globalcare-demo.com")
    other_doc = make_user("doc11@globalcare-demo.com", "pw", UserRole.DOCTOR)
    admin = make_user("admin_appt7@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient = make_patient()

    client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": patient.id},
        headers=auth_header(admin),
    )

    own = client.get(f"/api/v1/providers/{provider.id}/schedule", headers=auth_header(doc_user))
    assert own.status_code == 200
    assert len(own.json()) == 1

    denied = client.get(f"/api/v1/providers/{provider.id}/schedule", headers=auth_header(other_doc))
    assert denied.status_code == 403

    admin_view = client.get(f"/api/v1/providers/{provider.id}/schedule", headers=auth_header(admin))
    assert admin_view.status_code == 200

    not_found = client.get("/api/v1/providers/999999/schedule", headers=auth_header(admin))
    assert not_found.status_code == 404


def test_appointment_report(client, make_user, make_patient, auth_header, db_session):
    doc_user, provider = _make_provider(db_session, make_user, "doc12@globalcare-demo.com")
    admin = make_user("admin_appt8@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient = make_patient()

    appt = client.post(
        "/api/v1/appointments",
        json={"provider_id": provider.id, "scheduled_at": FUTURE, "patient_id": patient.id},
        headers=auth_header(admin),
    ).json()
    client.post(
        "/api/v1/consultations",
        json={"appointment_id": appt["id"], "summary": "s", "recommendations": "r"},
        headers=auth_header(doc_user),
    )

    denied = client.get("/api/v1/reports/appointments", headers=auth_header(doc_user))
    assert denied.status_code == 403

    report = client.get("/api/v1/reports/appointments", headers=auth_header(admin))
    assert report.status_code == 200
    body = report.json()
    assert body["total_appointments"] == 1
    assert body["total_consultations"] == 1
    assert body["appointments_by_status"] == {"completed": 1}
