from app.models.enums import UserRole


def test_registration_report_requires_admin_or_executive(client, make_user, auth_header):
    doctor = make_user("doc4@globalcare-demo.com", "pw", UserRole.DOCTOR)
    response = client.get("/api/v1/reports/registration", headers=auth_header(doctor))
    assert response.status_code == 403


def test_registration_report_reflects_real_data(
    client, make_user, make_patient, auth_header, db_session
):
    from app.models.facility import Facility
    from app.models.provider import Provider

    admin = make_user("admin8@globalcare-demo.com", "pw", UserRole.ADMINISTRATOR)

    facility = Facility(name="Report Facility", type="clinic", location="Nowhere")
    db_session.add(facility)
    db_session.commit()

    provider_user = make_user("doc5@globalcare-demo.com", "pw", UserRole.DOCTOR)
    provider = Provider(
        user_id=provider_user.id,
        full_name="Dr. Report",
        specialty="Oncology",
        facility_id=facility.id,
        license_ref="LIC-REPORT",
    )
    db_session.add(provider)
    db_session.commit()

    assigned_patient = make_patient(full_name="Assigned")
    assigned_patient.assigned_provider_id = provider.id
    db_session.commit()
    make_patient(full_name="Unassigned")

    response = client.get("/api/v1/reports/registration", headers=auth_header(admin))
    assert response.status_code == 200
    body = response.json()
    assert body["total_patients"] == 2
    assert body["total_providers"] == 1
    assert body["total_facilities"] == 1
    assert body["unassigned_patients"] == 1
    assert body["providers_by_specialty"] == {"Oncology": 1}
