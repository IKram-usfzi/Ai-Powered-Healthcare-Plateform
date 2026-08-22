#!/usr/bin/env bash
# Vulnerability-scans the built backend/frontend images with Trivy
# (docs/deccission.md ADR-009) and writes docs/security-scan-report.md.
# Requires Docker; Trivy itself runs containerized (aquasec/trivy), no local
# install needed.
set -euo pipefail
cd "$(dirname "$0")/.."

TRIVY_IMAGE="aquasec/trivy:0.58.0"
IMAGES=("infra-backend:latest" "infra-frontend:latest")
OUT_DIR="$(mktemp -d)"

for image in "${IMAGES[@]}"; do
  name="${image%%:*}"
  echo "Scanning ${image}..."
  docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "trivy-cache:/root/.cache/" \
    -v "${OUT_DIR}:/out" \
    "${TRIVY_IMAGE}" image \
    --severity CRITICAL,HIGH,MEDIUM,LOW \
    --format json \
    --output "/out/${name}.json" \
    "${image}"
done

python3 infra/generate_security_report.py "${OUT_DIR}" docs/security-scan-report.md
echo "Report written to docs/security-scan-report.md"
