package globalcare.authz

test_allow_role_when_role_is_in_the_allowed_list {
	allow_role with input as {"role": "administrator", "allowed_roles": ["administrator"]}
}

test_deny_role_when_role_is_not_in_the_allowed_list {
	not allow_role with input as {"role": "patient", "allowed_roles": ["administrator"]}
}

test_allow_role_when_one_of_several_roles_is_permitted {
	allow_role with input as {"role": "executive", "allowed_roles": ["administrator", "executive"]}
}

test_deny_role_on_empty_allowed_list {
	not allow_role with input as {"role": "administrator", "allowed_roles": []}
}

test_administrator_has_full_patient_access {
	allow_patient_access with input as {"role": "administrator"}
}

test_executive_has_aggregate_access {
	allow_patient_access with input as {"role": "executive"}
}

test_patient_can_access_own_record {
	allow_patient_access with input as {
		"role": "patient",
		"requesting_user_patient_id": 5,
		"target_patient_id": 5,
	}
}

test_patient_cannot_access_another_patients_record {
	not allow_patient_access with input as {
		"role": "patient",
		"requesting_user_patient_id": 5,
		"target_patient_id": 9,
	}
}

test_doctor_can_access_assigned_patient {
	allow_patient_access with input as {
		"role": "doctor",
		"requesting_provider_id": 3,
		"target_assigned_provider_id": 3,
	}
}

test_doctor_cannot_access_unassigned_patient {
	not allow_patient_access with input as {
		"role": "doctor",
		"requesting_provider_id": 3,
		"target_assigned_provider_id": 7,
	}
}

test_doctor_cannot_access_patient_with_no_assigned_provider {
	not allow_patient_access with input as {
		"role": "doctor",
		"requesting_provider_id": 3,
		"target_assigned_provider_id": null,
	}
}
