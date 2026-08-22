"""Load a sample of Synthea (MITRE) synthetic patients/providers/facilities and
derive health_readings from real Synthea vitals observations, per
docs/deccission.md ADR-005/ADR-011/ADR-017 and docs/impmemnentaion-plan.md Phase 1.

Run `python scripts/fetch_synthea.py` first to download the source CSVs.

heart_rate, systolic_bp, diastolic_bp, and glucose come directly from Synthea's
LOINC-coded observations (codes 8867-4, 8480-6, 8462-4, 2339-0). spo2 and
temperature are recorded in only ~5% of Synthea encounters (codes 2708-6,
8310-5), so where a patient/encounter lacks them, a physiologically plausible
value is simulated instead — this mirrors a real monitoring device recording a
full vitals bundle per reading, which raw Synthea data alone doesn't provide.

Usage:
    python scripts/seed_synthea.py --patients 200 --max-readings 5
"""

import argparse
import csv
import os
import random
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.security import hash_password  # noqa: E402
from app.db.base import Base, SessionLocal, engine  # noqa: E402
from app.models import Facility, HealthReading, Patient, Provider, User  # noqa: E402
from app.models.enums import UserRole  # noqa: E402

# See fetch_synthea.py's module docstring for why this isn't a fixed relative path.
DATA_DIR = Path(
    os.environ.get("SYNTHEA_DATA_DIR")
    or Path(__file__).resolve().parent.parent.parent / "data" / "synthea"
)
RAW_DIR = DATA_DIR / "raw" / "csv"

VITAL_CODES = {
    "8480-6": "systolic_bp",
    "8462-4": "diastolic_bp",
    "8867-4": "heart_rate",
    "2339-0": "glucose",
    "8310-5": "temperature",
    "2708-6": "spo2",
}

STRIP_TRAILING_DIGITS = re.compile(r"\d+$")


def clean_name(raw: str) -> str:
    return " ".join(STRIP_TRAILING_DIGITS.sub("", token) for token in raw.split())


def simulate_spo2() -> int:
    return random.randint(95, 99)


def simulate_temperature() -> float:
    return round(random.uniform(36.1, 37.2), 1)


def simulate_glucose() -> float:
    return round(random.uniform(75.0, 130.0), 1)


def load_organizations() -> dict[str, dict]:
    with open(RAW_DIR / "organizations.csv", newline="", encoding="utf-8") as f:
        return {row["Id"]: row for row in csv.DictReader(f)}


def load_providers(organizations: dict[str, dict], limit: int) -> list[dict]:
    with open(RAW_DIR / "providers.csv", newline="", encoding="utf-8") as f:
        rows = [row for row in csv.DictReader(f) if row["ORGANIZATION"] in organizations]
    return rows[:limit]


def load_patients(limit: int) -> list[dict]:
    with open(RAW_DIR / "patients.csv", newline="", encoding="utf-8") as f:
        rows = [row for row in csv.DictReader(f) if not row["DEATHDATE"]]
    return rows[:limit]


def load_vitals_by_patient_encounter(patient_ids: set[str]) -> dict[tuple[str, str], dict]:
    """Stream observations.csv once, keeping only rows for our selected patients."""
    grouped: dict[tuple[str, str], dict] = defaultdict(dict)
    with open(RAW_DIR / "observations.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["PATIENT"] not in patient_ids:
                continue
            field = VITAL_CODES.get(row["CODE"])
            if field is None:
                continue
            key = (row["PATIENT"], row["ENCOUNTER"])
            grouped[key][field] = (row["DATE"], row["VALUE"])
    return grouped


def seed(num_patients: int, max_readings: int) -> None:
    Base.metadata.create_all(engine)
    session = SessionLocal()

    print("Loading organizations/providers/patients from Synthea CSVs ...")
    organizations = load_organizations()
    provider_rows = load_providers(organizations, limit=50)
    patient_rows = load_patients(limit=num_patients)

    facility_by_org_id: dict[str, Facility] = {}
    for org_id in {p["ORGANIZATION"] for p in provider_rows}:
        org = organizations[org_id]
        facility = Facility(
            name=org["NAME"], type="hospital", location=f"{org['CITY']}, {org['STATE']}"
        )
        session.add(facility)
        facility_by_org_id[org_id] = facility
    session.flush()

    # Dev/demo login only — never a real credential. Lets every seeded provider log in
    # via POST /auth/login to exercise the Phase 2 API end-to-end.
    dev_password_hash = hash_password("ChangeMe123!")

    for row in provider_rows:
        user = User(
            email=f"provider+{row['Id'][:8]}@globalcare-demo.com",
            password_hash=dev_password_hash,
            role=UserRole.DOCTOR,
        )
        session.add(user)
        session.flush()
        session.add(
            Provider(
                user_id=user.id,
                full_name=clean_name(row["NAME"]),
                specialty=row["SPECIALITY"].title(),
                facility_id=facility_by_org_id[row["ORGANIZATION"]].id,
                license_ref=row["Id"][:12],
            )
        )

    patient_objs: dict[str, Patient] = {}
    for row in patient_rows:
        patient = Patient(
            full_name=f"{clean_name(row['FIRST'])} {clean_name(row['LAST'])}",
            date_of_birth=date.fromisoformat(row["BIRTHDATE"]),
            gender={"M": "Male", "F": "Female"}.get(row["GENDER"], row["GENDER"]),
            contact_info=f"{row['ADDRESS']}, {row['CITY']}, {row['STATE']} {row['ZIP']}",
        )
        session.add(patient)
        patient_objs[row["Id"]] = patient
    session.flush()

    print(f"Scanning observations.csv for vitals on {len(patient_objs)} patients ...")
    vitals = load_vitals_by_patient_encounter(set(patient_objs.keys()))

    reading_count = 0
    readings_per_patient: dict[str, int] = defaultdict(int)
    for (synthea_patient_id, _encounter_id), fields in vitals.items():
        if readings_per_patient[synthea_patient_id] >= max_readings:
            continue
        if not {"systolic_bp", "diastolic_bp", "heart_rate"} <= fields.keys():
            continue  # need the three commonly-recorded vitals at minimum

        recorded_at = datetime.fromisoformat(fields["heart_rate"][0].replace("Z", "+00:00"))
        session.add(
            HealthReading(
                patient_id=patient_objs[synthea_patient_id].id,
                heart_rate=round(float(fields["heart_rate"][1])),
                systolic_bp=round(float(fields["systolic_bp"][1])),
                diastolic_bp=round(float(fields["diastolic_bp"][1])),
                glucose=(
                    round(float(fields["glucose"][1]), 1)
                    if "glucose" in fields
                    else simulate_glucose()
                ),
                spo2=round(float(fields["spo2"][1])) if "spo2" in fields else simulate_spo2(),
                temperature=(
                    round(float(fields["temperature"][1]), 1)
                    if "temperature" in fields
                    else simulate_temperature()
                ),
                recorded_at=recorded_at,
            )
        )
        readings_per_patient[synthea_patient_id] += 1
        reading_count += 1

    session.commit()

    print(
        f"Seeded: {len(facility_by_org_id)} facilities, {len(provider_rows)} providers, "
        f"{len(patient_objs)} patients, {reading_count} health_readings."
    )
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patients", type=int, default=200)
    parser.add_argument("--max-readings", type=int, default=5)
    args = parser.parse_args()
    seed(num_patients=args.patients, max_readings=args.max_readings)
