from app.models.enums import UserRole

PATIENT_PAYLOAD = {
    "full_name": "John Doe",
    "date_of_birth": "1985-04-12",
    "gender": "Male",
    "contact_info": "123 Main St",
}


def test_create_patient_requires_admin(client, make_user, auth_header):
    doctor = make_user("doc1@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.post("/api/v1/patients", json=PATIENT_PAYLOAD, headers=auth_header(doctor))
    assert response.status_code == 403


def test_admin_can_create_and_read_patient(client, make_user, auth_header):
    admin = make_user("admin1@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    create = client.post("/api/v1/patients", json=PATIENT_PAYLOAD, headers=auth_header(admin))
    assert create.status_code == 201
    patient_id = create.json()["id"]
    assert create.json()["assigned_provider_id"] is None

    read = client.get(f"/api/v1/patients/{patient_id}", headers=auth_header(admin))
    assert read.status_code == 200
    assert read.json()["full_name"] == "John Doe"


def test_get_unknown_patient_404(client, make_user, auth_header):
    admin = make_user("admin2@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    response = client.get("/api/v1/patients/999999", headers=auth_header(admin))
    assert response.status_code == 404


def test_admin_can_update_patient(client, make_user, auth_header):
    admin = make_user("admin3@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)
    patient_id = client.post(
        "/api/v1/patients", json=PATIENT_PAYLOAD, headers=auth_header(admin)
    ).json()["id"]

    response = client.put(
        f"/api/v1/patients/{patient_id}",
        json={"contact_info": "456 New Ave"},
        headers=auth_header(admin),
    )
    assert response.status_code == 200
    assert response.json()["contact_info"] == "456 New Ave"
    assert response.json()["full_name"] == "John Doe"  # untouched fields preserved


def test_patient_can_read_own_record(client, make_user, make_patient, auth_header):
    patient_user = make_user("patient1@globalcare-demo.com", "pw", UserRole.PATIENT)
    patient = make_patient(user=patient_user)

    response = client.get(f"/api/v1/patients/{patient.id}", headers=auth_header(patient_user))
    assert response.status_code == 200


def test_patient_cannot_read_other_patient(client, make_user, make_patient, auth_header):
    patient_user = make_user("patient2@globalcare-demo.com", "pw", UserRole.PATIENT)
    make_patient(full_name="Self Patient", user=patient_user)
    other_patient = make_patient(full_name="Other Patient")

    response = client.get(f"/api/v1/patients/{other_patient.id}", headers=auth_header(patient_user))
    assert response.status_code == 403


def test_unauthenticated_request_rejected(client):
    response = client.get("/api/v1/patients")
    assert response.status_code == 401


def test_doctor_list_scoped_to_assigned_patients_only(
    client, make_user, make_patient, db_session, auth_header
):
    from app.models.facility import Facility
    from app.models.provider import Provider

    facility = Facility(name="Test Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()

    doctor_user = make_user("doc2@globalcare-demo.com", "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=doctor_user.id,
        full_name="Dr. Test",
        specialty="General",
        facility_id=facility.id,
        license_ref="LIC",
    )
    db_session.add(provider)
    db_session.commit()

    assigned = make_patient(full_name="Assigned Patient")
    assigned.assigned_provider_id = provider.id
    db_session.commit()
    make_patient(full_name="Unassigned Patient")  # not assigned to this doctor

    response = client.get("/api/v1/patients", headers=auth_header(doctor_user))
    assert response.status_code == 200
    names = [p["full_name"] for p in response.json()]
    assert names == ["Assigned Patient"]
