from app.models.enums import UserRole


def _facility(db_session):
    from app.models.facility import Facility

    facility = Facility(name="Test Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()
    return facility


PROVIDER_PAYLOAD = {
    "email": "dr.jones@globalcare-demo.com",
    "password": "DoctorPass123!",
    "full_name": "Dr. Jones",
    "specialty": "Pediatrics",
    "license_ref": "LIC-100",
}


def test_create_provider_requires_admin(client, make_user, auth_header, db_session):
    facility = _facility(db_session)
    doctor = make_user("doc3@globalcare-demo.com", "pw", UserRole.DOCTOR)
    payload = {**PROVIDER_PAYLOAD, "facility_id": facility.id}
    response = client.post("/api/v1/providers", json=payload, headers=auth_header(doctor))
    assert response.status_code == 403


def test_admin_creates_provider_and_it_can_log_in(client, make_user, auth_header, db_session):
    facility = _facility(db_session)
    admin = make_user("admin4@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    payload = {**PROVIDER_PAYLOAD, "facility_id": facility.id}

    create = client.post("/api/v1/providers", json=payload, headers=auth_header(admin))
    assert create.status_code == 201
    assert create.json()["specialty"] == "Pediatrics"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": PROVIDER_PAYLOAD["email"], "password": PROVIDER_PAYLOAD["password"]},
    )
    assert login.status_code == 200


def test_duplicate_provider_email_conflicts(client, make_user, auth_header, db_session):
    facility = _facility(db_session)
    admin = make_user("admin5@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    payload = {**PROVIDER_PAYLOAD, "facility_id": facility.id}

    first = client.post("/api/v1/providers", json=payload, headers=auth_header(admin))
    assert first.status_code == 201
    second = client.post("/api/v1/providers", json=payload, headers=auth_header(admin))
    assert second.status_code == 409


def test_list_providers_requires_admin_or_executive(client, make_user, auth_header):
    patient_user = make_user("patient3@globalcare-demo.com", "pw", UserRole.PATIENT)
    response = client.get("/api/v1/providers", headers=auth_header(patient_user))
    assert response.status_code == 403


def test_assign_patient_to_provider(client, make_user, make_patient, auth_header, db_session):
    facility = _facility(db_session)
    admin = make_user("admin6@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    payload = {
        **PROVIDER_PAYLOAD,
        "facility_id": facility.id,
        "email": "dr.assign@globalcare-demo.com",
    }
    provider_id = client.post("/api/v1/providers", json=payload, headers=auth_header(admin)).json()[
        "id"
    ]
    patient = make_patient()

    response = client.post(
        f"/api/v1/providers/{provider_id}/assign-patient",
        json={"patient_id": patient.id},
        headers=auth_header(admin),
    )
    assert response.status_code == 200
    assert response.json()["assigned_provider_id"] == provider_id


def test_assign_patient_unknown_provider_404(client, make_user, make_patient, auth_header):
    admin = make_user("admin7@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient = make_patient()
    response = client.post(
        "/api/v1/providers/999999/assign-patient",
        json={"patient_id": patient.id},
        headers=auth_header(admin),
    )
    assert response.status_code == 404
