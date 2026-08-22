"""Download the Synthea (MITRE) CSV sample dataset — the project's primary
synthetic data source (docs/deccission.md ADR-005/ADR-011/ADR-017).

Source: the official synthea-sample-data GitHub Pages/API mirror, not
synthea.mitre.org directly (that host's TLS chain didn't validate from this
sandbox — see PROJECT_CONTEXT.md).

Usage:
    python scripts/fetch_synthea.py
"""

import urllib.request
import zipfile
from pathlib import Path

DOWNLOAD_URL = (
    "https://synthetichealth.github.io/synthea-sample-data/"
    "downloads/synthea_sample_data_csv_apr2020.zip"
)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "synthea"
RAW_DIR = DATA_DIR / "raw"
ZIP_PATH = RAW_DIR / "synthea_sample_data_csv_apr2020.zip"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not ZIP_PATH.exists():
        print(f"Downloading {DOWNLOAD_URL} ...")
        urllib.request.urlretrieve(DOWNLOAD_URL, ZIP_PATH)
    else:
        print(f"Already downloaded: {ZIP_PATH}")

    print("Extracting patients/providers/organizations/observations CSVs ...")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        members = [
            m
            for m in zf.namelist()
            if m.endswith(
                ("patients.csv", "providers.csv", "organizations.csv", "observations.csv")
            )
        ]
        zf.extractall(RAW_DIR, members=members)

    print(f"Done. Files extracted under {RAW_DIR}")


if __name__ == "__main__":
    main()
