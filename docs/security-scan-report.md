# Security Scan Report (Trivy)

**Related:** `Security.md` §6, `deccission.md` ADR-009

Generated 2026-08-22 by `infra/trivy_scan.sh` against the images built by `infra/docker-compose.yml` (`docker compose build`). Every image is a real scan result, not a hand-authored placeholder — the counts below reflect whatever Trivy's vulnerability database currently knows about the pinned base images and dependencies.

## Summary

| Image | Critical | High | Medium | Low |
|---|---|---|---|---|
| `infra-backend:latest` | 3 | 57 | 73 | 68 |
| `infra-frontend:latest` | 9 | 72 | 142 | 85 |

## infra-backend:latest — Critical/High findings

| Severity | CVE | Package | Installed | Fixed in |
|---|---|---|---|---|
| CRITICAL | CVE-2026-13221 | perl-base | 5.40.1-6 | not yet available |
| CRITICAL | CVE-2026-42496 | perl-base | 5.40.1-6 | not yet available |
| CRITICAL | CVE-2026-8376 | perl-base | 5.40.1-6 | not yet available |
| HIGH | CVE-2024-23342 | ecdsa | 0.19.2 | not yet available |
| HIGH | CVE-2025-62727 | starlette | 0.41.3 | 0.49.1 |
| HIGH | CVE-2025-69720 | libncursesw6 | 6.5+20250216-2 | not yet available |
| HIGH | CVE-2025-69720 | libtinfo6 | 6.5+20250216-2 | not yet available |
| HIGH | CVE-2025-69720 | ncurses-base | 6.5+20250216-2 | not yet available |
| HIGH | CVE-2025-69720 | ncurses-bin | 6.5+20250216-2 | not yet available |
| HIGH | CVE-2026-14456 | libssl3t64 | 3.5.6-1~deb13u2 | not yet available |
| HIGH | CVE-2026-14456 | openssl | 3.5.6-1~deb13u2 | not yet available |
| HIGH | CVE-2026-14456 | openssl-provider-legacy | 3.5.6-1~deb13u2 | not yet available |
| HIGH | CVE-2026-23949 | jaraco.context | 5.3.0 | 6.1.0 |
| HIGH | CVE-2026-24049 | wheel | 0.45.1 | 0.46.2 |
| HIGH | CVE-2026-32274 | black | 24.10.0 | 26.3.1 |
| HIGH | CVE-2026-41992 | gzip | 1.13-1 | not yet available |
| HIGH | CVE-2026-42497 | perl-base | 5.40.1-6 | not yet available |
| HIGH | CVE-2026-48818 | starlette | 0.41.3 | 1.1.0 |
| HIGH | CVE-2026-48962 | perl-base | 5.40.1-6 | not yet available |
| HIGH | CVE-2026-53612 | bsdutils | 1:2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | libblkid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | liblastlog2-2 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | libmount1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | libsmartcols1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | libuuid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | login | 1:4.16.0-2+really2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | mount | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53612 | util-linux | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | bsdutils | 1:2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | libblkid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | liblastlog2-2 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | libmount1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | libsmartcols1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | libuuid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | login | 1:4.16.0-2+really2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | mount | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53613 | util-linux | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | bsdutils | 1:2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | libblkid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | liblastlog2-2 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | libmount1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | libsmartcols1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | libuuid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | login | 1:4.16.0-2+really2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | mount | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53614 | util-linux | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | bsdutils | 1:2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | libblkid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | liblastlog2-2 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | libmount1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | libsmartcols1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | libuuid1 | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | login | 1:4.16.0-2+really2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | mount | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-53615 | util-linux | 2.41-5 | 2.41.5-0+deb13u1 |
| HIGH | CVE-2026-54283 | starlette | 0.41.3 | 1.3.1 |
| HIGH | CVE-2026-54369 | libacl1 | 2.3.2-2+b1 | not yet available |
| HIGH | CVE-2026-57432 | perl-base | 5.40.1-6 | not yet available |
| HIGH | CVE-2026-57433 | perl-base | 5.40.1-6 | not yet available |
| HIGH | CVE-2026-9538 | perl-base | 5.40.1-6 | not yet available |

## infra-frontend:latest — Critical/High findings

| Severity | CVE | Package | Installed | Fixed in |
|---|---|---|---|---|
| CRITICAL | CVE-2023-45853 | zlib1g | 1:1.2.13.dfsg-1 | not yet available |
| CRITICAL | CVE-2024-24790 | stdlib | v1.20.12 | 1.21.11, 1.22.4 |
| CRITICAL | CVE-2025-68121 | stdlib | v1.20.12 | 1.24.13, 1.25.7, 1.26.0-rc.3 |
| CRITICAL | CVE-2026-13221 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| CRITICAL | CVE-2026-33845 | libgnutls30 | 3.7.9-2+deb12u6 | 3.7.9-2+deb12u7 |
| CRITICAL | CVE-2026-42010 | libgnutls30 | 3.7.9-2+deb12u6 | 3.7.9-2+deb12u7 |
| CRITICAL | CVE-2026-42496 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| CRITICAL | CVE-2026-59873 | tar | 6.2.1 | 7.5.19 |
| CRITICAL | CVE-2026-8376 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| HIGH | CVE-2023-45288 | stdlib | v1.20.12 | 1.21.9, 1.22.2 |
| HIGH | CVE-2024-21538 | cross-spawn | 7.0.3 | 7.0.5, 6.0.6 |
| HIGH | CVE-2024-34156 | stdlib | v1.20.12 | 1.22.7, 1.23.1 |
| HIGH | CVE-2025-61726 | stdlib | v1.20.12 | 1.24.12, 1.25.6 |
| HIGH | CVE-2025-61729 | stdlib | v1.20.12 | 1.24.11, 1.25.5 |
| HIGH | CVE-2025-64756 | glob | 10.4.2 | 11.1.0, 10.5.0 |
| HIGH | CVE-2025-69720 | libtinfo6 | 6.4-4 | not yet available |
| HIGH | CVE-2025-69720 | ncurses-base | 6.4-4 | not yet available |
| HIGH | CVE-2025-69720 | ncurses-bin | 6.4-4 | not yet available |
| HIGH | CVE-2026-13149 | brace-expansion | 2.0.1 | 5.0.7, 1.1.16, 2.1.2 |
| HIGH | CVE-2026-14257 | brace-expansion | 2.0.1 | 5.0.8, 3.0.3, 2.1.3, 1.1.17 |
| HIGH | CVE-2026-23745 | tar | 6.2.1 | 7.5.3 |
| HIGH | CVE-2026-23950 | tar | 6.2.1 | 7.5.4 |
| HIGH | CVE-2026-24842 | tar | 6.2.1 | 7.5.7 |
| HIGH | CVE-2026-25679 | stdlib | v1.20.12 | 1.25.8, 1.26.1 |
| HIGH | CVE-2026-26960 | tar | 6.2.1 | 7.5.8 |
| HIGH | CVE-2026-26996 | minimatch | 9.0.5 | 10.2.1, 9.0.6, 8.0.5, 7.4.7, 6.2.1, 5.1.7, 4.2.4, 3.1.3 |
| HIGH | CVE-2026-27145 | stdlib | v1.20.12 | 1.25.11, 1.26.4 |
| HIGH | CVE-2026-27903 | minimatch | 9.0.5 | 10.2.3, 9.0.7, 8.0.6, 7.4.8, 6.2.2, 5.1.8, 4.2.5, 3.1.3 |
| HIGH | CVE-2026-27904 | minimatch | 9.0.5 | 10.2.3, 9.0.7, 8.0.6, 7.4.8, 6.2.2, 5.1.8, 4.2.5, 3.1.4 |
| HIGH | CVE-2026-29786 | tar | 6.2.1 | 7.5.10 |
| HIGH | CVE-2026-31802 | tar | 6.2.1 | 7.5.11 |
| HIGH | CVE-2026-32280 | stdlib | v1.20.12 | 1.25.9, 1.26.2 |
| HIGH | CVE-2026-32281 | stdlib | v1.20.12 | 1.25.9, 1.26.2 |
| HIGH | CVE-2026-32283 | stdlib | v1.20.12 | 1.25.9, 1.26.2 |
| HIGH | CVE-2026-33811 | stdlib | v1.20.12 | 1.25.10, 1.26.3 |
| HIGH | CVE-2026-33814 | stdlib | v1.20.12 | 1.25.10, 1.26.3 |
| HIGH | CVE-2026-33818 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-33846 | libgnutls30 | 3.7.9-2+deb12u6 | 3.7.9-2+deb12u7 |
| HIGH | CVE-2026-3833 | libgnutls30 | 3.7.9-2+deb12u6 | 3.7.9-2+deb12u7 |
| HIGH | CVE-2026-39820 | stdlib | v1.20.12 | 1.25.10, 1.26.3 |
| HIGH | CVE-2026-39821 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-39822 | stdlib | v1.20.12 | 1.25.12, 1.26.5, 1.27.0-rc.2 |
| HIGH | CVE-2026-39836 | stdlib | v1.20.12 | 1.25.10, 1.26.3 |
| HIGH | CVE-2026-41992 | gzip | 1.12-1 | not yet available |
| HIGH | CVE-2026-42009 | libgnutls30 | 3.7.9-2+deb12u6 | 3.7.9-2+deb12u7 |
| HIGH | CVE-2026-42497 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| HIGH | CVE-2026-42499 | stdlib | v1.20.12 | 1.25.10, 1.26.3 |
| HIGH | CVE-2026-42504 | stdlib | v1.20.12 | 1.25.11, 1.26.4 |
| HIGH | CVE-2026-4878 | libcap2 | 1:2.66-4+deb12u2+b2 | 1:2.66-4+deb12u3 |
| HIGH | CVE-2026-48815 | sigstore | 2.3.1 | 4.1.1 |
| HIGH | CVE-2026-48962 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| HIGH | CVE-2026-53571 | vite | 5.4.21 | 8.0.16, 7.3.5, 6.4.3 |
| HIGH | CVE-2026-53613 | bsdutils | 1:2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | libblkid1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | libmount1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | libsmartcols1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | libuuid1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | mount | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | util-linux | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53613 | util-linux-extra | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | bsdutils | 1:2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | libblkid1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | libmount1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | libsmartcols1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | libuuid1 | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | mount | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | util-linux | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-53615 | util-linux-extra | 2.38.1-5+deb12u3 | not yet available |
| HIGH | CVE-2026-54369 | libacl1 | 2.3.1-3 | not yet available |
| HIGH | CVE-2026-56853 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-56858 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-56859 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-56860 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-56862 | stdlib | v1.20.12 | 1.25.13, 1.26.6, 1.27.0-rc.3 |
| HIGH | CVE-2026-57432 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| HIGH | CVE-2026-57433 | perl-base | 5.36.0-7+deb12u3 | not yet available |
| HIGH | CVE-2026-59874 | tar | 6.2.1 | 7.5.18 |
| HIGH | CVE-2026-69152 | brace-expansion | 2.0.1 | 1.1.18, 2.1.4, 3.0.6, 5.0.9 |
| HIGH | CVE-2026-69192 | ip-address | 9.0.5 | 10.3.1 |
| HIGH | CVE-2026-73566 | tar | 6.2.1 | 7.5.21 |
| HIGH | CVE-2026-9538 | perl-base | 5.36.0-7+deb12u3 | not yet available |

## Notes

- This is a point-in-time scan of a student capstone proof-of-concept using synthetic data only (`Security.md` §1) — findings are documented transparently rather than suppressed, consistent with this project's practice of reporting real limitations (see the AI model's thin `high`-risk class in `docs/ai-evaluation-report.md`).
- Medium/Low severity findings are counted above but not itemized here; re-run `infra/trivy_scan.sh` and inspect the raw JSON for full detail on any entry.
- Base images are pinned (`postgres:16-alpine`, `redis:7-alpine`, `python:3.11-slim`, `node:*` per the Dockerfiles) so re-scanning after a `docker compose build --pull` periodically is the primary remediation path for OS-package CVEs.
