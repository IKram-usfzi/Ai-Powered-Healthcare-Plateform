package globalcare.authz

# docs/deccission.md ADR-006/ADR-024: a narrow, explicit set of Rego policies,
# not a general policy platform. allow_role backs backend/app/api/deps.py's
# require_roles() dependency, used at every role-gated endpoint. See
# authz_test.rego for the unit tests (`opa test infra/opa/policies`).

default allow_role = false

allow_role {
	input.role == input.allowed_roles[_]
}

# allow_patient_access is not wired into the API today (row-level checks stay
# in the API layer per Security.md §9 and ADR-024's fail-closed-at-DB-query
# reasoning) but is authored and tested here per Security.md §3's named
# example policies, and is available for a future call site to consume.
default allow_patient_access = false

# Administrators have full CRUD over registration data (Security.md §3).
allow_patient_access {
	input.role == "administrator"
}

# Executives read aggregate data only — dashboards/reports never pass a
# target_patient_id, so this rule never fires for an individual record.
allow_patient_access {
	input.role == "executive"
}

# A patient may access only their own record.
allow_patient_access {
	input.role == "patient"
	input.requesting_user_patient_id == input.target_patient_id
}

# A doctor may access only patients assigned to them.
allow_patient_access {
	input.role == "doctor"
	input.target_assigned_provider_id != null
	input.requesting_provider_id == input.target_assigned_provider_id
}
