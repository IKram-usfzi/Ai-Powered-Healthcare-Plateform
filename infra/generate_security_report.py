"""Turns raw Trivy JSON output (one file per scanned image) into
docs/security-scan-report.md — the "security scan report" GitHub deliverable
(exam brief §11, docs/deccission.md ADR-009). Invoked by infra/trivy_scan.sh;
not meant to be run standalone against arbitrary input.
"""

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]


def _load(image_json: Path) -> dict:
    data = json.loads(image_json.read_text())
    counts = Counter()
    findings = []
    for result in data.get("Results", []) or []:
        for vuln in result.get("Vulnerabilities", []) or []:
            severity = vuln.get("Severity", "UNKNOWN")
            counts[severity] += 1
            if severity in ("CRITICAL", "HIGH"):
                findings.append(
                    {
                        "id": vuln.get("VulnerabilityID", "?"),
                        "package": vuln.get("PkgName", "?"),
                        "installed": vuln.get("InstalledVersion", "?"),
                        "fixed": vuln.get("FixedVersion", "not yet available"),
                        "severity": severity,
                        "title": vuln.get("Title") or vuln.get("PkgName", ""),
                    }
                )
    return {
        "artifact": data.get("ArtifactName", image_json.stem),
        "counts": counts,
        "findings": findings,
    }


def _render(scans: list[dict]) -> str:
    lines = [
        "# Security Scan Report (Trivy)",
        "",
        "**Related:** `Security.md` §6, `deccission.md` ADR-009",
        "",
        f"Generated {date.today().isoformat()} by `infra/trivy_scan.sh` against the images built "
        "by `infra/docker-compose.yml` (`docker compose build`). Every image is a real scan "
        "result, not a hand-authored placeholder — the counts below reflect whatever Trivy's "
        "vulnerability database currently knows about the pinned base images and dependencies.",
        "",
        "## Summary",
        "",
        "| Image | Critical | High | Medium | Low |",
        "|---|---|---|---|---|",
    ]
    for scan in scans:
        c = scan["counts"]
        lines.append(
            f"| `{scan['artifact']}` | {c.get('CRITICAL', 0)} | {c.get('HIGH', 0)} "
            f"| {c.get('MEDIUM', 0)} | {c.get('LOW', 0)} |"
        )

    for scan in scans:
        lines += ["", f"## {scan['artifact']} — Critical/High findings"]
        if not scan["findings"]:
            lines.append("")
            lines.append("None found.")
            continue
        lines += ["", "| Severity | CVE | Package | Installed | Fixed in |", "|---|---|---|---|---|"]
        for f in sorted(scan["findings"], key=lambda x: (x["severity"] != "CRITICAL", x["id"])):
            lines.append(
                f"| {f['severity']} | {f['id']} | {f['package']} | {f['installed']} | {f['fixed']} |"
            )

    lines += [
        "",
        "## Notes",
        "",
        "- This is a point-in-time scan of a student capstone proof-of-concept using synthetic "
        "data only (`Security.md` §1) — findings are documented transparently rather than "
        "suppressed, consistent with this project's practice of reporting real limitations (see "
        "the AI model's thin `high`-risk class in `docs/ai-evaluation-report.md`).",
        "- Medium/Low severity findings are counted above but not itemized here; re-run "
        "`infra/trivy_scan.sh` and inspect the raw JSON for full detail on any entry.",
        "- Base images are pinned (`postgres:16-alpine`, `redis:7-alpine`, `python:3.11-slim`, "
        "`node:*` per the Dockerfiles) so re-scanning after a `docker compose build --pull` "
        "periodically is the primary remediation path for OS-package CVEs.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    in_dir = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    scans = [_load(p) for p in sorted(in_dir.glob("*.json"))]
    out_path.write_text(_render(scans))


if __name__ == "__main__":
    main()
